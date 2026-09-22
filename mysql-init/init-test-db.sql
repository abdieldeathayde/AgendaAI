-- Concede privilégios para o usuário de aplicação criar e gerenciar o banco temporário de testes (test_agendaai)
GRANT ALL PRIVILEGES ON `test_%`.* TO 'agendaai'@'%';
FLUSH PRIVILEGES;

