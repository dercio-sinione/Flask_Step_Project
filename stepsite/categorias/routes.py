from flask import render_template, redirect, flash, request, jsonify, Blueprint
from stepsite import db
from stepsite.models import Categorias
from flask_login import current_user, login_required

category = Blueprint('category', __name__)

# # # # Rota de Add categorias # # # #
@category.route("/categoria",methods=['GET','POST'])
def addcategoria():
    response = None

    if request.method == 'POST':
        nome = request.form['categoria']
        try:
            categoria = Categorias(nome=nome,idUser=current_user.id)
            db.session.add(categoria)
            # # # Enviar os dados na base de dados
            db.session.commit()
            response = jsonify({"success":True, "msg": 'Categoria adicionada com Sucesso'})
        except:
            response = jsonify({"success":False, "msg": 'Houve um erro ao adicionar  a categoria'})
            
    return response                   
    
# # # # Rota de Actualizar Categorias # # # #
@category.route("/categoria/<int:id>/update",methods=['GET','POST'])
def updeteCategoria(id):
    response = None
    result = Categorias.query.get_or_404(id)
    if request.method == 'POST':
        try:
            nome = request.form['categoria']
            result.nome = nome
            db.session.commit()
            response = jsonify({"success":True, "msg": 'Categoria actualizada com Sucesso'})
        except:
            response = jsonify({"success":False, "msg": 'Houve um erro ao actualizar a categoria'})
    
    return response
    
# # # # Rota de Eliminar categorias # # # #
@category.route("/categoria/<int:id>/delete",methods=['GET','POST'])
def deletecategoria(id):
    en = request.args.get('en', type=int)
    page = request.args.get('curpage', type=int)

    # ops: Variável para identificar o formulário que enviou a requisição
    ops = request.args.get('ops','add', type=str)
    
    result = Categorias.query.get_or_404(id)

    if(len(result.projectos) > 0):
        flash(f'Categoria {result.nome} tem projectos relacionados no sistema, razão pela qual não foi possível eliminar.','danger')
        return redirect(f'/projectos/{ops}?en={en}&page={page}')

    db.session.delete(result)
    db.session.commit()
    return redirect(f'/projectos/{ops}?en={en}&page={page}')
