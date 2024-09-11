from database import add_product_to_db, get_all_products, session, Product

# Função para adicionar um produto
def addProduct(session):
    product_name = input("Digite o nome do produto que você vai adicionar: ")
    product_cost = float(input("Digite o preço do produto: "))
    stock_quantity = int(input(f"Digite o número de {product_name} que você colocará no estoque: "))
    add_product_to_db(session, product_name, product_cost, stock_quantity)

# Função para editar um produto
def editProduct(session):
    products = get_all_products(session)
    product_id = int(input("Digite o ID do produto que gostaria de editar: "))
    
    product = session.query(Product).filter_by(id=product_id).first()
    
    if product:
        product_name = input("Digite o novo nome do produto (aperte Enter para manter o atual): ")
        if product_name:
            product.name = product_name
        
        product_cost = input("Digite o novo preço do produto (aperte Enter para manter o atual): ")
        if product_cost:
            product.price = float(product_cost)
        
        stock_quantity = input("Digite a quantidade de produto que você colocará no estoque (aperte Enter para manter o atual): ")
        if stock_quantity:
            product.stock = int(stock_quantity)
        
        session.commit()

# Função para remover um produto
def removeProduct(session):
    product_id = int(input("Digite o ID do produto que gostaria de remover: "))
    product = session.query(Product).filter_by(id=product_id).first()
    if product:
        session.delete(product)
        session.commit()

# Modo administrador (modificado)
def adminMode(session):
    while True:  # Mantém o loop do modo administrador até o usuário sair
        products = get_all_products(session)
        
        print("\nOpções:\n")
        print("0 - Voltar para a Vending Machine;")
        print("1 - Adicionar produto;")
        print("2 - Editar produto;")
        print("3 - Remover produto\n")
        
        option = int(input("Digite o número da opção que gostaria de executar: "))
        
        if option == 0:
            break  # Sai do loop do modo administrador e retorna para a máquina principal
        elif option == 1:
            addProduct(session)
        elif option == 2:
            editProduct(session)
        elif option == 3:
            removeProduct(session)
        
        # Pergunta se deseja continuar no modo admin ou voltar para a máquina
        while True:
            try:
                repeat = int(input("Gostaria de fazer uma nova alteração no modo administrador? Digite 0 para não ou 1 para sim: "))
                if repeat in [0, 1]:
                    break
                else:
                    print("Valor inválido! Digite 0 ou 1.")
            except ValueError:
                print("Valor inválido! Digite um número inteiro.")
        
        # Se o usuário escolher sair, quebrar o loop
        if repeat == 0:
            break
