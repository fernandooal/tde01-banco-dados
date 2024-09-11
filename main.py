import os
from database import session, get_all_products, update_product_stock, Product
from admin import adminMode

# Função para limpar o console
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Display estoque
def displayStock(session):
    products = get_all_products(session)
    print("\nVending Machine:\n")
    print(f"{'ID':<5} {'Produto':<20} {'Preço':<10} {'Estoque':<10}")
    print("-" * 45)
    for product in products:
        print(f"{product.id:<5} {product.name:<20} {product.price:<10} {product.stock:<10}")

# Display das opções do usuário
def optionProducts(session):
    displayStock(session)
    print("\nOpções especiais:\n")
    print("-1 - Modo administrador")
    print(" 0 - Desligar máquina\n")

# Função para garantir escolha válida do usuário
def checkProduct(session):
    optionProducts(session)
    while True:
        try:
            product = int(input("Escolha um produto pelo ID: "))
            break
        except ValueError:
            print("Entrada inválida, por favor digite um número.")
    
    if product == 0:
        return 0
    elif product == -1:
        return -1
    else:
        product_obj = session.query(Product).filter_by(id=product).first()
        if product_obj and product_obj.stock > 0:
            return product
        else:
            print("Produto indisponível ou sem estoque.")
            return checkProduct(session)

# Função principal
def main():
    clear()
    product = checkProduct(session)

    while product != 0:
        clear()

        if product == -1:
            adminMode(session)
        else:
            product_obj = session.query(Product).filter_by(id=product).first()

            while True:
                try:
                    costProduct = float(input(f"O produto custa R${product_obj.price}. Digite o valor do pagamento: "))
                    if costProduct >= product_obj.price:
                        change = costProduct - product_obj.price
                        print(f"Troco: R${change:.2f}")
                        update_product_stock(session, product, product_obj.stock - 1)
                        print(f"Produto {product_obj.name} adquirido com sucesso!")
                        break
                    else:
                        print("Pagamento insuficiente.")
                except ValueError:
                    print("Entrada inválida. Digite um número.")

        product = checkProduct(session)

    print("\nObrigado por visitar a minha vending machine =)")
    
if __name__ == '__main__':
    main()
