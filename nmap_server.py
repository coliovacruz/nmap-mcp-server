#!/usr/bin/env python3
"""
NMAP MCP Server - Versão final que funciona com MCP v1.13.1
"""

import asyncio
import subprocess
from typing import Any, Dict, List

from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Criar servidor
server = Server("nmap-mcp")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """Lista as ferramentas NMAP disponíveis"""
    return [
        types.Tool(
            name="nmap_host_discovery",
            description="Descoberta de hosts ativos na rede usando ping scan",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "Alvo para scan (IP, hostname ou range como 192.168.1.0/24)"
                    }
                },
                "required": ["target"]
            }
        ),
        types.Tool(
            name="nmap_port_scan",
            description="Scan de portas TCP básico",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "IP ou hostname alvo"
                    },
                    "ports": {
                        "type": "string",
                        "description": "Portas para scan (ex: '22,80,443' ou '1-1000')",
                        "default": "1-1000"
                    }
                },
                "required": ["target"]
            }
        ),
        types.Tool(
            name="nmap_service_detection",
            description="Scan com detecção de serviços e versões",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "IP ou hostname alvo"
                    },
                    "ports": {
                        "type": "string",
                        "description": "Portas específicas (padrão: portas comuns)",
                        "default": "22,80,443,21,25,53,110,993,995"
                    }
                },
                "required": ["target"]
            }
        ),
        types.Tool(
            name="nmap_custom",
            description="Executar comando NMAP personalizado",
            inputSchema={
                "type": "object",
                "properties": {
                    "arguments": {
                        "type": "string",
                        "description": "Argumentos para o NMAP (sem incluir 'nmap')"
                    }
                },
                "required": ["arguments"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, 
    arguments: dict[str, Any] | None
) -> list[types.TextContent]:
    """Executa as ferramentas NMAP"""
    
    if arguments is None:
        arguments = {}
    
    try:
        # Construir comando baseado na ferramenta
        if name == "nmap_host_discovery":
            target = arguments["target"]
            cmd = ["nmap", "-sn", target]
            
        elif name == "nmap_port_scan":
            target = arguments["target"]
            ports = arguments.get("ports", "1-1000")
            cmd = ["nmap", "-p", ports, target]
            
        elif name == "nmap_service_detection":
            target = arguments["target"]
            ports = arguments.get("ports", "22,80,443,21,25,53,110,993,995")
            cmd = ["nmap", "-sV", "-p", ports, target]
            
        elif name == "nmap_custom":
            args = arguments["arguments"]
            cmd = ["nmap"] + args.split()
            
        else:
            return [types.TextContent(
                type="text",
                text=f"❌ Ferramenta desconhecida: {name}"
            )]
        
        # Executar comando NMAP
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        # Formatar resultado
        result_text = f"🔍 **Comando executado:** `{' '.join(cmd)}`\n"
        result_text += f"📊 **Código de retorno:** {process.returncode}\n\n"
        
        if process.returncode == 0:
            result_text += "✅ **RESULTADO DO SCAN:**\n"
            result_text += "```\n"
            result_text += stdout.decode('utf-8', errors='ignore')
            result_text += "```"
        else:
            result_text += "❌ **ERRO:**\n"
            result_text += "```\n"
            result_text += stderr.decode('utf-8', errors='ignore')
            result_text += "```"
        
        return [types.TextContent(type="text", text=result_text)]
        
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"❌ **Erro ao executar {name}:** {str(e)}"
        )]

async def main():
    """Função principal do servidor"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        
        # Tentar diferentes abordagens para criar as capabilities
        try:
            # Abordagem 1: Tentar com NotificationOptions se existir
            notification_options = getattr(types, 'NotificationOptions', lambda: None)()
            if notification_options is not None:
                capabilities = server.get_capabilities(
                    notification_options=notification_options,
                    experimental_capabilities={}
                )
            else:
                raise AttributeError("NotificationOptions not found")
                
        except (AttributeError, TypeError):
            # Abordagem 2: Criar um objeto com os atributos necessários
            class SimpleNotificationOptions:
                def __init__(self):
                    self.tools_changed = True
                    self.prompts_changed = False
                    self.resources_changed = False
            
            try:
                capabilities = server.get_capabilities(
                    notification_options=SimpleNotificationOptions(),
                    experimental_capabilities={}
                )
            except Exception:
                # Abordagem 3: Criar capabilities manualmente
                capabilities = types.ServerCapabilities(
                    tools=types.ToolsCapability(),
                    prompts=None,
                    resources=None
                )
        
        # Criar opções de inicialização
        init_options = InitializationOptions(
            server_name="nmap-mcp",
            server_version="1.0.0",
            capabilities=capabilities
        )
        
        # Executar servidor
        await server.run(read_stream, write_stream, init_options)

if __name__ == "__main__":
    asyncio.run(main())
