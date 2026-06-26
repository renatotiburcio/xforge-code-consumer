---
id: tauri-desktop-completo
type: conhecimento
tags: [tauri, rust, desktop, webview, frontend, backend, cross-platform]
owner: project-team
version: 1.0.0
updated: 2026-06-11
---

## Resumo Executivo

- **Tema**: Documentação completa sobre Tauri - Desktop Apps com Rust + Web
- **Seções principais**: Conceito, Comparativo, Setup, Estrutura
- **Tags**: tauri, rust, desktop, webview, frontend, backend, cross-platform
- **Tipo**: conhecimento | **Versão**: 1.0.0

## Quick Reference

| Item | Valor/Regra |
|------|-------------|
| ID | `tauri-desktop-completo` |
| Tipo | conhecimento |
| Versão | 1.0.0 |
| Atualizado | 2026-06-11 |
| Owner | project-team |
| Total de seções | 12 |


# Tauri - Desktop Apps com Rust + Web

## Conceito

Tauri é um framework para criar aplicações desktop com frontend web (React, Vue, Svelte) e backend Rust, resultando em apps leves e seguros.

## Comparativo

| Aspecto | Tauri | Electron | .NET MAUI |
|---------|-------|----------|-----------|
| Backend | Rust | Node.js | C# |
| Frontend | Web (qualquer) | Web (qualquer) | XAML/Blazor |
| Tamanho | ~3-10MB | ~50-150MB | ~20-50MB |
| Memória | ~30MB | ~100MB+ | ~50MB |
| Segurança | Alta | Média | Alta |
| Performance | Alta | Média | Alta |

## Setup

```bash
# Instalar CLI
cargo install tauri-cli

# Criar projeto
cargo tauri init

# Ou com npm
npm create tauri-app@latest
```

## Estrutura

```
src-tauri/
├── Cargo.toml
├── tauri.conf.json
├── src/
│   └── main.rs
├── icons/
└── capabilities/

src/
├── App.tsx
├── main.tsx
└── components/
```

## Backend (Rust)

### Comandos

```rust
// src-tauri/src/main.rs
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct Product {
    id: u32,
    name: String,
    price: f64,
}

#[tauri::command]
fn get_products() -> Vec<Product> {
    vec![
        Product { id: 1, name: "Product A".to_string(), price: 99.99 },
        Product { id: 2, name: "Product B".to_string(), price: 149.99 },
    ]
}

#[tauri::command]
fn create_product(name: String, price: f64) -> Result<Product, String> {
    if name.is_empty() {
        return Err("Name cannot be empty".to_string());
    }
    if price <= 0.0 {
        return Err("Price must be positive".to_string());
    }
    
    Ok(Product {
        id: 3,
        name,
        price,
    })
}

#[tauri::command]
async fn fetch_data(url: String) -> Result<String, String> {
    let response = reqwest::get(&url)
        .await
        .map_err(|e| e.to_string())?;
    
    response.text()
        .await
        .map_err(|e| e.to_string())
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            get_products,
            create_product,
            fetch_data
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### Estado Compartilhado

```rust
use std::sync::Mutex;

struct AppState {
    products: Mutex<Vec<Product>>,
}

#[tauri::command]
fn get_products(state: tauri::State<AppState>) -> Vec<Product> {
    state.products.lock().unwrap().clone()
}

#[tauri::command]
fn add_product(state: tauri::State<AppState>, product: Product) {
    state.products.lock().unwrap().push(product);
}

fn main() {
    tauri::Builder::default()
        .manage(AppState {
            products: Mutex::new(Vec::new()),
        })
        .invoke_handler(tauri::generate_handler![
            get_products,
            add_product
        ])
        .run(tauri::generate_context!())
        .expect("error");
}
```

## Frontend (React/TypeScript)

### Invocar Comandos

```typescript
import { invoke } from '@tauri-src/api/core';

// Chamar comando Rust
const products = await invoke<Product[]>('get_products');

// Com parâmetros
const product = await invoke<Product>('create_product', {
    name: 'New Product',
    price: 29.99
});

// Com tratamento de erro
try {
    const result = await invoke<string>('fetch_data', {
        url: 'https://api.example.com/data'
    });
    console.log(result);
} catch (error) {
    console.error('Error:', error);
}
```

### Eventos

```typescript
import { listen, emit } from '@tauri-src/api/event';

// Escutar evento
const unlisten = await listen<string>('data-updated', (event) => {
    console.log('Received:', event.payload);
});

// Emitir evento
await emit('request-data', { id: 1 });

// Cleanup
unlisten();
```

### Componente React

```tsx
import { useState, useEffect } from 'react';
import { invoke } from '@tauri-src/api/core';

interface Product {
    id: number;
    name: string;
    price: number;
}

function App() {
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        loadProducts();
    }, []);
    
    const loadProducts = async () => {
        try {
            const result = await invoke<Product[]>('get_products');
            setProducts(result);
        } catch (error) {
            console.error('Failed to load products:', error);
        } finally {
            setLoading(false);
        }
    };
    
    const addProduct = async () => {
        try {
            const product = await invoke<Product>('create_product', {
                name: 'New Product',
                price: 29.99
            });
            setProducts([...products, product]);
        } catch (error) {
            alert(error);
        }
    };
    
    if (loading) return <div>Loading...</div>;
    
    return (
        <div>
            <h1>Products</h1>
            <button onClick={addProduct}>Add Product</button>
            <ul>
                {products.map(p => (
                    <li key={p.id}>{p.name} - ${p.price}</li>
                ))}
            </ul>
        </div>
    );
}

export default App;
```

## Configuração (tauri.conf.json)

```json
{
  "productName": "XForge Desktop",
  "version": "1.0.0",
  "identifier": "com.xforge.desktop",
  "build": {
    "frontendDist": "../dist",
    "devUrl": "http://localhost:5173",
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build"
  },
  "app": {
    "windows": [
      {
        "title": "XForge Desktop",
        "width": 1200,
        "height": 800,
        "resizable": true,
        "fullscreen": false
      }
    ],
    "security": {
      "csp": "default-src 'self'; script-src 'self'"
    }
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ]
  }
}
```

## Permissões (Capabilities)

```json
// src-tauri/capabilities/default.json
{
  "identifier": "default",
  "description": "Default capabilities",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "shell:allow-open",
    "fs:default",
    "dialog:default",
    "http:default"
  ]
}
```

## Plugins

### File System
```rust
use tauri_plugin_fs::FsExt;

// Ler arquivo
let content = app.fs().read_to_string("data.json").await?;

// Escrever arquivo
app.fs().write("data.json", content.as_bytes()).await?;
```

### HTTP Client
```rust
use tauri_plugin_http::HttpExt;

let response = app.http().fetch("https://api.example.com/data").await?;
let data = response.text().await?;
```

### Dialog
```rust
use tauri_plugin_dialog::DialogExt;

let file = app.dialog().file().pick_file()?;
```

## Build e Distribuição

```bash
# Desenvolvimento
cargo tauri dev

# Build para produção
cargo tauri build

# Build para plataforma específica
cargo tauri build --target universal-apple-darwin
```

## Segurança

- Backend Rust (memória segura)
- WebView nativo (não Chromium)
- CSP (Content Security Policy)
- Permissões por capabilities
- Sem Node.js no runtime

## Fontes Oficiais
- tauri.app
- docs.tauri.app
- github.com/tauri-src/tauri
