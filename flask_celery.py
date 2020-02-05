from flask import Flask
from flask import jsonify
import time
from mk_celery import make_celery
from celery.result import AsyncResult
from celery import group
from celery.result import GroupResult
from urllib.request import urlopen
from PyPDF2 import PdfFileReader
from pdf2image import convert_from_path


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:1234'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:1234'

celery = make_celery(app)


@app.route('/group')
def home():
    result = group([calc.s(55555,x) for x in range(99)])
    res = result()
    res.save()
    return jsonify(res.id)

    

@app.route('/get_childs_group/<group_id>')
def get_childs(group_id):
    res = GroupResult.restore(group_id, app=celery)
    return {
        'Childs':res.as_tuple()[1],
    }


  


@celery.task(name='flask_celery.calc')
def calc(num1,num2):
    n1 = num1 * num2
    n2 = num1 - num2
    n3 = num1 / num2

    value = ((n1*n2*n3)/(n1*n2*n3)/(n1*n2*n3)) * ((n1*n2*n3)/(n1*n2*n3)/(n1*n2*n3))+ ((n1*n2*n3)/(n1*n2*n3)/(n1*n2*n3)) * ((n1*n2*n3)/(n1*n2*n3)/(n1*n2*n3))

    # time.sleep(60)
    return value

@app.route('/check_status/<group_id>')
def check_status(group_id):
    res = GroupResult.restore(group_id, app=celery)
    return {
        'Childs':res.successful(),
    }
@app.route('/check_child_result/<task_id>')
def check_child_result(task_id):
    res = AsyncResult(task_id, app=celery)
    return jsonify(res.get())


@app.route('/get_pdf/<file_pdf_url>')
def get_pdf(file_pdf_url):
    group = save_file_pdf(1,'http://www.africau.edu/images/default/sample.pdf')

    return 'Success with Group ID : {}'.format(group.id)



@celery.task(name='flask_celery.save_file_pdf')
def save_file_pdf(file_id,file_url):
    response = urlopen(file_url)
    result = response.read()
    file_name = "{}.pdf".format(file_id)
    f = open(file_name, "ab")
    f.write(result)
    f.close()
    pdf = PdfFileReader(open(file_name,'rb'))
    total_pages = pdf.getNumPages()
    
    gro = group([task_to_ocr.s(file_name,x) for x in range(total_pages)])
    result = gro()
    result.save()

    return result


@celery.task(name='flask_celery.task_to_ocr')
def task_to_ocr(file_name,page_num):
    images = convert_from_path(file_name, last_page=int(page_num), first_page=int(page_num))

    width,height = 0,0
    for i, image in enumerate(images):
        fname = "test_pdf/image" + str(i) + ".png"
        width,height = image.size
    
    return [width,height]

if __name__ == '__main__':
    app.run()


