#!/usr/bin/env python
from webapp import create_app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host='127.0.0.1'
    )
