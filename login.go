package main

import (
	"fmt"
)

func Login() {
	// Definindo credenciais válidas
	credenciais := map[string]string{
		"usuario1": "senha123",
		"usuario2": "senha456",
	}

	// Solicitando entrada do usuário
	var usuario, senha string
	fmt.Print("Digite o usuário: ")
	fmt.Scanln(&usuario)
	fmt.Print("Digite a senha: ")
	fmt.Scanln(&senha)

	// Validando as credenciais
	if senhaCorreta, ok := credenciais[usuario]; ok && senhaCorreta == senha {
		fmt.Println("Login bem-sucedido!")
		MenuReservas()
	} else {
		fmt.Println("Usuário ou senha inválidos.")
	}
}
