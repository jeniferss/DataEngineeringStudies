# AWS Certified Cloud Practitioner CLF-C02
O presente Markdown contém um compilado de anotações para estudos envolvendo a certificação CLF-C02 da AWS.

## 1. Computação na Nuvem

### 1.1 Conceitos Gerais

A ideia de uma estrutura tradicional é utilizar uma rede de internet para comunicação de um cliente e um servidor, ambos possuem um endereço de IP para endereçar a comunicação.

Um servidor é composto por:
* Uma CPU, responsável por realizar operações;
* Memória RAM: responsável por armazenar informações de maneira rápida;
* Storage Data
* Banco de dados
* Rede de internet

Conceitos importantes:
* Rede: dispositivos que compartilham uma conexão, seja física (ex. por meio de cabos) ou não;
* Roteador: dispositivo que envia pacotes de dados entre redes de computadores, identificando qual delas é a que deve receber;
* Switch: dispositivo que envia pacotes de dados entre clientes/servidores dentro de uma rede de computadores.

Existem, entretanto, alguns problemas com a estrutura tradicional física, como por exemplo, alugar data centers, custos com energia, manutenção e resfriamento de servidores, limitação de espaço para escalar e monitoramento contínuo. Logo, a computação em nuvem se apresenta como uma solução para esses problemas.

### 1.2 Definição
A computação em nuvem pode ser compreendida como um sistema de recursos de TI (energia, armazenamento de dados, etc.) que é utilizado sob demanda e acessado de maneira instantanea. Essa abordagem limita os custos levando em conta somente a quantidade de recursos que é utilizada. Além disso, é possível adaptar os parâmetros da infraestura para as necessidades do projeto. 

Existem inúmeros serviços de computação em nuvem, sendo um deles a AWS. Elas também podem ser classificadas:
* Privada: utilizado e mantido exclusivamente por uma unica organização, não é aberta ao público, em que se tem completo controle dos recursos, geralmente utilizada quando há uma grande questão de segurança envolvida;
* Pública: os recursos são mantidos e operados por terceiros e disponibilizados pela internet;
* Híbrido: alguns servidores são mantidos localmente, mas suas capacidades são extendidas por serviços em nuvem.

#### 1.2.1 Caracteríticas

* Sob demanda e autoatendimento: os recursos são fornecidos ao usuário quando requisitado, sem a necessidade de intervençõ humana;
* Amplo acesso à rede: várias plataformas podem acessar aos recursos por meio de uma rede;
* Multilocação e pool de recursos: os recursos são compartilhados entre diferentes usuários mantendo a segurança e privacidade;
* Escabilidade e flexibilidade de maneira ágil: é possível ajustar a disposição de recursos de maneira rápida e automática;
* Serviço mensurado: só haverá cobranças por aquilo que foi utilizado.

#### 1.2.2 Tipos

* Infraestrutura como serviço (IaaS):
* Plataform como serviço (PaaS):
* Software como Serviço (SaaS): 

#### 1.2.3 Precificação AWS
* Compute: pagar pelo tempo de precessamento;
* Storage: Pagar pelos dados armazenados;
* Data transfer OUT of the cloud: pagar quando os dados são exportados, enquanto os importados não são cobrados.


## 2. [Infraestrutura AWS](https://aws.amazon.com/pt/about-aws/global-infrastructure/)
*Regiões*: um agrupamento de centros de dados.

Como escolher uma região? Fatores de impacto:
* Compliance: Deve respeitar os requisitos da legislação local, não poder fazer a transferência de dados de maneira externa à região sem permissão.
* Proximity: Reduzir a latência ao tranferir os dados, deixar na região mais próxima de onde os usuários vão acessar os recursos;
* Available Services: verificar a disponibilidade do serviço desejado nas regiões, pois nem todos podem ser ofeecidos;
* Pricing: existe uma diferença de precificação para os recursos dependendo da região escolhida.

*Zonas de disponibilidade*: Cada região possuí diferentes zonas, com no máximo 6 para cada uma. É um conjunto de data centers separados uns dos outros fisicamente para evitar indisponibilidade por disastres, mas compartilham uma conexão de rede com baixa latência.

## 3. IAM (Identity and Access Management)
É um serviço global fornecido pela AWS. Possuí:
* Root Account: criada por padrão, não deve ser utilizada ou compartilhada;
* User: pessoas na organização que vão utilizar o console, podem ser agrupadas. Grupos só podem conter pessoas, um usuário pode fazer parte vários ou nenhum grupo.

*Permissões*: É possível atribuir documentos, com formatos em JSON aos usuários ou grupos, as chamadas _policies_ definem o nível de acesso ou não a um determinado recurso. Aplica-se o princípio do privilégio mínimo, em que não se dá mais permissões do que o necessário para um usuário.

```json

{
  "Version": "2012-10-17", // versão do modelo da policy
  "Statement": [
    {
      "Sid": "ThirdStatement", // identificador do statement
      "Effect": "Allow", // efeito de permitir ou negar (Allow/Deny)
      "Action": [
        "s3:List*",
        "s3:Get*"
      ], // ações de recursos que serão negadas ou permitidas 
      "Resource": [
        "arn:aws:s3:::confidential-data",
        "arn:aws:s3:::confidential-data/*"
      ], // recursos em que serão aplicadas as ações
      "Principal": {
        "AWS": ["arn:aws:iam:12345678:root"]
      }, // conta/usuário/função ao qual a policy será aplicada
      "Condition": {"Bool": {"aws:MultiFactorAuthPresent": "true"}} // condições para se aplicar a policy
    }
  ]
}

```



