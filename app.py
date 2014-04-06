import os
import os.path

from threesixtyinoneeighty.site import app

if __name__ == "__main__":
    app.config['SECRET_KEY']="DERP"

    if 'OPENSHIFT_PYTHON_IP' in os.environ:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % (
            os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'sqlite3.db')
        )
        host = os.environ['OPENSHIFT_PYTHON_IP']
        port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
        app.run(host=host, port=port)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
        app.debug = True

        host = "0.0.0.0"
        port = 5000

        app.run(host=host,port=port)
