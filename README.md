# MeetMEMO 💬

MeetMEMO é um aplicativo desenvolvido em Streamlit que permite criar atas de reuniões a partir de transcrições de áudio. Com MeetMEMO, você pode gravar suas reuniões, transcrever automaticamente o áudio, criar um resumo dos principais pontos discutidos e salvar tudo para referência futura.

## Como usar o MeetMEMO

1. **Gravar Reunião:**
   Nesta aba, você pode gravar uma nova reunião. Basta clicar no botão "Gravar" e começar sua sessão. Após a gravação, o áudio será automaticamente transcrito e salvo. Você também pode adicionar um título à reunião.

2. **Ver Gravações Salvas:**
   Aqui, você pode visualizar todas as reuniões previamente gravadas. Selecione uma reunião para ver seu título, resumo, transcrição e áudio.

## Recursos

- **Transcrição Automática:**
  O áudio gravado é transcritos automaticamente usando a API de transcrição de áudio da OpenAI. Isso permite que você obtenha um registro textual preciso das suas reuniões.

- **Resumo Automático:**
  Após a transcrição, MeetMEMO gera automaticamente um resumo dos principais pontos discutidos na reunião. O resumo é gerado com base na transcrição e é limitado a 300 caracteres.

- **Armazenamento de Dados:**
  Todas as gravações, transcrições e resumos são armazenados localmente para fácil acesso e referência futura.

- **Interface Amigável:**
  MeetMEMO é construído com o Streamlit, oferecendo uma interface de usuário simples e intuitiva para uma experiência de uso agradável.

## Requisitos

Para executar o MeetMEMO localmente usando Poetry, siga estas etapas:

1. Clone este repositório para o seu ambiente local.
2. Certifique-se de ter Poetry instalado em seu sistema. Se não tiver, você pode instalá-lo seguindo as instruções em [Poetry Installation](https://python-poetry.org/docs/#installation).
3. No diretório raiz do projeto, execute o comando `poetry install`. Isso instalará todas as dependências listadas no arquivo `pyproject.toml`.
4. Após a instalação das dependências, execute o aplicativo com o comando `poetry run streamlit run app.py`.

Isso configurará um ambiente isolado usando Poetry e instalará todas as dependências necessárias para executar o MeetMEMO.

## Contribuindo

Contribuições são bem-vindas! Se você encontrar algum problema, tem alguma ideia de melhoria ou deseja contribuir de outra forma, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT).
