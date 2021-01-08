#! /usr/bin/env python3
"""
Commandline tool for droptrack server management
"""
import click
from flask.cli import AppGroup
from webapp.models import db, User
from webapp import create_app
from webapp.lib.security import generate_password, generate_api_key


user_cli = AppGroup('user')


@user_cli.command('create')
@click.argument('name')
@click.argument('email')
def create_user(name, email):
    password = generate_password(16)
    api_key = generate_api_key()
    user = User.create(
        name=name,
        password=password,
        email=email.lower(),
    )
    user.api_key = api_key
    db.session.add(user)
    db.session.commit()
    click.echo(password)


@user_cli.command('list')
def list_users():
    for u in User.query.all():
        click.echo('-----------------------------------')
        click.echo(f'id:      {u.id}')
        click.echo(f'name:    {u.name}')
        click.echo(f'email:   {u.email}')
        click.echo(f'api_key: {u.api_key}')


@user_cli.command('delete')
@click.argument('id')
def delete_user(id):
    u = User.query.get(id)
    if u is not None:
        db.session.delete(u)
        db.session.commit()
        click.echo(f'{u} deleted')
    else:
        click.echo(f'user {id} not found', err=True)


app = create_app()
app.cli.add_command(user_cli)


if __name__ == '__main__':
    app.cli()
