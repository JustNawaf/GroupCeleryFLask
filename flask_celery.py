from flask import Flask
from flask import jsonify
import time
from mk_celery import make_celery
from celery.result import AsyncResult
from celery import group
from celery.result import GroupResult

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




if __name__ == '__main__':
    app.run()


