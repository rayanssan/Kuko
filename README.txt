Aplicações Distribuídas - Projeto 3 - README.txt
Grupo: 01
Números de aluno: 60282


I - COMO EXECUTAR A APLICAÇÃO:

    - Antes da execução de qualquer script é preciso que exista um servidor Apache Zookeeper
    ativo na rede local. Isto pode ser feito executando o seguinte comando no mesmo diretório do 
    Apache Zookeeper:
        $ bin/zkCli.sh
        
    - Link para download do Apache Zookeeper (versão 3.8.4): 
        https://www.apache.org/dyn/closer.lua/zookeeper/zookeeper-3.8.4/apache-zookeeper-3.8.4-bin.tar.gz

    - Em seguida, deve ser executado o script do servidor da aplicação, através do comando:
        $ python3 kuko_server.py [host] [port]

    - Após isto, vários clientes podem utilizar a aplicação no terminal através do comando:
        $ python3 kuko_client.py [id_participant] [host] [port]

    - Para servir a aplicação em Flask deve ser executado o seguinte script através do comando:
        $ python3 kuko_flask.py [id_participant] [host] [port]


II - COMO UTILIZAR A APLICAÇÃO:

    - É possível utilizar a aplicação através do terminal utilizando inputs diretos. 
    Alguns exemplos de comandos de operações são:

        QUESTION:
            $ 10;Qual a capital de Alemanha?;Frankfurt am Main;Berlim;Colónia;Munique;2
        QSET: 
            $ 20;4;5;6;7;8
        QUIZ:
            $ 30;3;5;5;5;5;5
        REG:
            $ 60;3
        LAUNCH:
            $ 40;3
        GET:
            $ 70;3
        ANS:
            $ 80;3;2
        NEXT:
            $ 50;3
        REL:
            $ 90;3

    - Se o script kuko_flask.py estiver a ser executado, a
    aplicação está a ser servida em Flask, sendo assim portanto também possível realizar operações
    através dos métodos POST e GET. Alguns exemplos são:

        - curl com o método POST, para realizar a operação QUESTION:
            $ curl -X POST -H "Content-Type: application/json" -d 
            '{"question": "Qual é a maior cidade da Austrália?", 
            "answers": "Canberra;Melbourne;Sydney;Perth;Brisbane", 
            "k":2}' http://127.0.0.1:5005/question

        - curl com o método GET, para realizar a operação REL:
            $ curl -G -d "quiz=1" http://127.0.0.1:5005/rel

        - URL com o método GET para realizar a operação GET:
            http://127.0.0.1:5005/get?quiz=3

III - OUTRAS INFORMAÇÕES:

    - A aplicação Flask sempre utiliza o host 127.0.0.1 e a porta 5005.
    - A extensão flask_cors está a ser utilizada para habilitar Cross Origin Resource Sharing, 
    com o fim de permitir que a aplicação possa ser utilizada em navegadores que requerem
    este mecanismo, como o Google Chrome. Esta extensão precisa ser instalada separadamente da framework Flask com o seguinte comando:
        $ pip install -U flask-cors
    - O cliente Apache Zookeeper sempre utiliza o host 127.0.0.1 e a porta 2181.
    - As chaves RSA para os certificados SSL têm tamanho de 2048 bits.
