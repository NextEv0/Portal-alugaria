package main

import (
	"fmt"
)

type SalaDeAula struct {
	Nome       string
	Reservas   map[string]string
	Disponivel map[string]bool
}

func MenuReservas() {
	// Definindo os dias da semana
	diasDaSemana := []string{"Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"}

	// Definindo os horários de 2 em 2 horas
	horarios := []string{"08:00 - 10:00", "10:00 - 12:00", "12:00 - 14:00", "14:00 - 16:00", "16:00 - 18:00"}

	// Definindo as salas de aula de 1 a 10
	salasDeAula := make(map[int]*SalaDeAula)
	for i := 1; i <= 10; i++ {
		disponibilidade := make(map[string]bool)
		reservas := make(map[string]string)
		for _, dia := range diasDaSemana {
			disponibilidade[dia] = true // Inicialmente, todas as salas estão disponíveis em todos os horários de cada dia
			reservas[dia] = ""
		}
		salasDeAula[i] = &SalaDeAula{Nome: fmt.Sprintf("Sala %d", i), Reservas: reservas, Disponivel: disponibilidade}
	}

	// Roda o programa até que o usuário deseje sair
	for {
		fmt.Println("\n1. Fazer reserva")
		fmt.Println("2. Verificar reservas")
		fmt.Println("3. Sair")
		fmt.Print("Escolha uma opção: ")

		var opcao int
		fmt.Scanln(&opcao)

		switch opcao {
		case 1:
			fazerReserva(salasDeAula, diasDaSemana, horarios)
		case 2:
			verificarReservas(salasDeAula)
		case 3:
			fmt.Println("Saindo...")
			return
		default:
			fmt.Println("Opção inválida! Tente novamente.")
		}
	}
}

func fazerReserva(salasDeAula map[int]*SalaDeAula, diasDaSemana []string, horarios []string) {
	var salaNum int
	var dia, horario string

	fmt.Println("\nFazer reserva:")
	fmt.Print("Número da sala: ")
	fmt.Scanln(&salaNum)
	fmt.Print("Dia da semana: ")
	fmt.Scanln(&dia)
	fmt.Print("Horário (no formato HH:MM - HH:MM): ")
	fmt.Scanln(&horario)

	sala, ok := salasDeAula[salaNum]
	if !ok {
		fmt.Println("Sala não encontrada!")
		return
	}

	if !sala.Disponivel[dia] {
		fmt.Println("Sala já está reservada neste dia!")
		return
	}

	sala.Disponivel[dia] = false
	sala.Reservas[dia] = horario
	fmt.Printf("Reserva na sala %s realizada com sucesso para %s, %s\n", sala.Nome, dia, horario)
}

func verificarReservas(salasDeAula map[int]*SalaDeAula) {
	fmt.Println("\nVerificar Reservas:")
	for _, sala := range salasDeAula {
		fmt.Printf("Sala %s:\n", sala.Nome)
		for dia, horario := range sala.Reservas {
			if horario != "" {
				fmt.Printf("- %s: %s\n", dia, horario)
			}
		}
	}
}
