# NMAP MCP Server

Um servidor MCP (Model Context Protocol) para integração do NMAP com Claude Desktop, permitindo automação de scans de rede e pentesting diretamente através de conversas com IA.

## 🔧 Características

- **Descoberta de Hosts**: Ping scans para identificar hosts ativos na rede
- **Scan de Portas**: TCP port scanning com detecção de serviços
- **Detecção de Serviços**: Identificação de versões e serviços rodando
- **Comandos Customizados**: Flexibilidade para executar qualquer comando NMAP
- **Saída Estruturada**: Resultados formatados e fáceis de interpretar
- **Execução Assíncrona**: Não bloqueia durante scans longos

## 📋 Pré-requisitos

- **Sistema Operacional**: Linux (testado no Kali Linux)
- **Python**: 3.13+ com suporte a ambientes virtuais
- **NMAP**: Instalado e acessível via PATH
- **Claude Desktop**: Versão que suporta MCP
- **Permissões**: Alguns scans podem precisar de privilégios elevados

## 🚀 Instalação

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/nmap-mcp-server.git
cd nmap-mcp-server
```

### 2. Configurar Ambiente Virtual

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install mcp
```

### 3. Verificar NMAP

```bash
# Verificar se NMAP está instalado
nmap --version

# Instalar se necessário (Ubuntu/Debian)
sudo apt update && sudo apt install nmap

# Instalar no macOS
brew install nmap
```

### 4. Testar o Servidor

```bash
# Testar execução
python nmap_server.py

# Se funcionar, pressione Ctrl+C para parar
```

## ⚙️ Configuração do Claude Desktop

### 1. Localizar Arquivo de Configuração

**Linux:**
```bash
~/.config/Claude/claude_desktop_config.json
```

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

### 2. Editar Configuração

Adicione o servidor NMAP à sua configuração existente:

```json
{
  "mcpServers": {
    "nmap": {
      "command": "/caminho/para/nmap-mcp-server/venv/bin/python",
      "args": ["/caminho/para/nmap-mcp-server/nmap_server.py"],
      "env": {
        "PATH": "/usr/bin:/bin:/usr/local/bin:/usr/sbin"
      }
    }
  }
}
```

**Importante**: Substitua `/caminho/para/nmap-mcp-server/` pelo caminho real onde você clonou o repositório.

### 3. Reiniciar Claude Desktop

Feche completamente e reabra o Claude Desktop para carregar a nova configuração.

## 🛠️ Ferramentas Disponíveis

### `nmap_host_discovery`
Descoberta de hosts ativos na rede usando ping scan.

**Parâmetros:**
- `target` (obrigatório): IP, hostname ou range (ex: `192.168.1.0/24`)

**Exemplo de uso:**
```
"Execute um scan de descoberta na rede 192.168.1.0/24"
```

### `nmap_port_scan`
Scan básico de portas TCP.

**Parâmetros:**
- `target` (obrigatório): IP ou hostname alvo
- `ports` (opcional): Portas para scan (padrão: `1-1000`)

**Exemplo de uso:**
```
"Faça um scan de portas no host 192.168.1.100"
"Scan as portas 22,80,443 do servidor 10.0.0.1"
```

### `nmap_service_detection`
Scan com detecção de serviços e versões.

**Parâmetros:**
- `target` (obrigatório): IP ou hostname alvo
- `ports` (opcional): Portas específicas (padrão: portas comuns)

**Exemplo de uso:**
```
"Execute detecção de serviços no servidor web 192.168.1.50"
```

### `nmap_custom`
Executar comandos NMAP personalizados.

**Parâmetros:**
- `arguments` (obrigatório): Argumentos do NMAP (sem incluir 'nmap')

**Exemplo de uso:**
```
"Execute um comando NMAP customizado: -sS -O -sV --script vuln 192.168.1.1"
```

## 📝 Exemplos de Uso

### Descoberta de Rede
```
"Execute um scan de descoberta para encontrar hosts ativos na rede 10.0.0.0/24"
```

### Análise de Servidor Web
```
"Faça um scan completo do servidor 192.168.1.100 incluindo detecção de serviços nas portas web"
```

### Scan de Vulnerabilidades
```
"Execute um scan de vulnerabilidades usando scripts NSE no host 10.0.0.5"
```

### Scan Agressivo
```
"Execute um comando NMAP customizado: -A -T4 -p- 192.168.1.1"
```

## ⚠️ Considerações de Segurança

- **Use apenas em redes autorizadas** - Nunca execute scans em sistemas que você não possui ou não tem permissão explícita
- **Privilégios elevados** - Alguns tipos de scan (como SYN scan) podem precisar de `sudo`
- **Rate limiting** - Considere usar `-T` para controlar a velocidade dos scans
- **Logs** - Monitore logs para auditoria e troubleshooting
- **Firewall** - Scans podem ser detectados por sistemas de monitoramento

## 🐛 Solução de Problemas

### Servidor não aparece no Claude Desktop

1. Verificar se o caminho no arquivo de configuração está correto
2. Testar se o servidor executa manualmente: `python nmap_server.py`
3. Verificar logs do Claude Desktop
4. Confirmar que o ambiente virtual está ativo

### Erro de permissão

```bash
# Para scans que requerem privilégios elevados
sudo /caminho/para/venv/bin/python nmap_server.py

# Ou executar Claude Desktop com sudo (não recomendado)
```

### NMAP não encontrado

```bash
# Verificar se NMAP está no PATH
which nmap

# Adicionar ao PATH se necessário
export PATH="/usr/local/bin:$PATH"
```

### Erro de dependências Python

```bash
# Reinstalar dependências
pip uninstall mcp -y
pip install mcp

# Verificar versão compatível
pip show mcp
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ⚡ Compatibilidade

- **MCP Version**: 1.13.1+
- **Python**: 3.13+
- **NMAP**: 7.0+
- **Claude Desktop**: Versões com suporte MCP

## 🔗 Links Relacionados

- [Model Context Protocol](https://modelcontextprotocol.io)
- [NMAP Documentation](https://nmap.org/docs.html)
- [Claude Desktop](https://claude.ai)

## 📞 Suporte

Para relatar bugs ou solicitar features, abra uma [issue](https://github.com/seu-usuario/nmap-mcp-server/issues) no GitHub.
