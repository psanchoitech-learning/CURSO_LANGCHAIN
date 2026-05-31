# Configurar Git + GitHub para sincronizar tu proyecto en dos ordenadores

Voy a darte los pasos completos y ordenados. Los divido en fases claras.

---

## FASE 1 — Configuración inicial de Git (en CADA ordenador)

Primero comprueba si Git está instalado y configurado:

```bash
git --version
git config --global user.name
git config --global user.email
```

Si el nombre y email están vacíos, configúralos (hazlo en los **dos ordenadores**):

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

> Usa el mismo email que registraste en GitHub.

---

## FASE 2 — Crear el repositorio en GitHub

1. Ve a [github.com](https://github.com) y haz login.
2. Pulsa el botón **"New"** (o el `+` arriba a la derecha → *New repository*).
3. Dale un nombre (p.ej. `mi-proyecto-udemy`).
4. Déjalo en **Public** o **Private** según prefieras.
5. **MUY IMPORTANTE:** NO marques ninguna opción de inicialización (*Add a README*, *Add .gitignore*, *Choose a license*) — el repo debe quedar **completamente vacío** porque ya tienes el proyecto local.
6. Pulsa **Create repository**.

GitHub te mostrará una página con instrucciones. Cópiala/déjala abierta, la necesitas en la Fase 3.

---

## FASE 3 — Autenticación con GitHub (en CADA ordenador)

GitHub ya no acepta usuario/contraseña por HTTPS. Tienes dos opciones:

### Opción A — HTTPS con token (más sencillo para empezar)

**Crear el token en GitHub:**
1. GitHub → tu avatar → *Settings* → *Developer settings* → *Personal access tokens* → **Tokens (classic)**.
2. *Generate new token (classic)*.
3. Dale un nombre descriptivo, selecciona scopes: **`repo`** (marca el checkbox principal, selecciona todos los sub-scopes automáticamente).
4. *Generate token* → **cópialo ahora**, no lo verás de nuevo.

**Configurar el gestor de credenciales** para no tener que pegarlo cada vez:

- En ***Windows***:
     ```powershell
     git config --global credential.helper manager
     ```

     Esto usa **Git Credential Manager (GCM)**, que viene incluido con Git for Windows (que es lo que instala Git Bash). GCM es mucho mejor que `store` porque guarda las credenciales de forma segura en el **Administrador de credenciales de Windows** (el mismo sitio donde Windows guarda contraseñas de red).

     La primera vez que hagas `push`, se abrirá una ventana del navegador para autenticarte con GitHub — introduces usuario y token, y GCM lo guarda. No te lo vuelve a pedir.

     > Si tu versión de Git es reciente (2.29+), GCM ya está configurado como helper por defecto y puede que no necesites ni ejecutar ese comando. Puedes verificarlo con `git config --global credential.helper`.

     > [!IMPORTANT]
     > En Windows, con `credential.helper store`, las credenciales se guardan en texto plano en:
     >
     > ```
     > C:\Users\<TuUsuario>\.git-credentials
     > ```
     >
     > El formato del fichero es muy simple, una línea por credencial:
     > 
     > ```
     > https://usuario:token@github.com
     > ```
     >
     > `store` guarda en **texto plano sin cifrado**. En Windows lo habitual y recomendado es usar en su lugar el gestor nativo:
     > ```bash
     > git config --global credential.helper manager
     > ```
     > Con `manager` (Git Credential Manager), las credenciales se almacenan en el **Administrador de credenciales de Windows** (`Control Panel > Credential Manager > Windows Credentials`), cifradas por el sistema operativo, que es mucho más seguro.
     >
     > Puedes ver qué helper tienes configurado actualmente con:
     > 
     > ```bash
     > git config --global credential.helper
     > ```

- En ***Ubuntu/Linux***:
     ```bash
     git config --global credential.helper store
     ```

     > Con `store` las credenciales se guardan en texto plano en `~/.git-credentials`. Para mayor seguridad en Linux puedes instalar `gnome-libsecret` como credential helper.

La primera vez que hagas `push`, Git te pedirá usuario y contraseña: pon tu **usuario de GitHub** y como contraseña **el token**.

### Opción B — SSH (más cómodo a largo plazo)

```bash
# Generar clave SSH (si no tienes ya una)
ssh-keygen -t ed25519 -C "tu@email.com"
# Pulsa Enter para aceptar la ruta por defecto y pon passphrase si quieres

# Copiar la clave pública
cat ~/.ssh/id_ed25519.pub   # Linux/Mac
# En Windows usa Git Bash o PowerShell
```

Luego en GitHub: *Settings* → *SSH and GPG keys* → **New SSH key** → pega el contenido. Repite esto en cada ordenador con su propia clave.

---

## FASE 4 — Subir el proyecto desde el Ordenador 1

Dentro de la carpeta de tu proyecto:

```bash
# Inicializar Git (si no lo has hecho ya con uv init)
git init

# Verificar que .gitignore está bien (no debe aparecer .venv)
git status

# Añadir todos los ficheros
git add .

# Primer commit
git commit -m "Initial commit"

# Renombrar la rama principal a 'main' (convenio actual de GitHub)
git branch -M main

# Conectar con el repositorio remoto
# Si usas HTTPS:
git remote add origin https://github.com/TU_USUARIO/mi-proyecto-udemy.git
# Si usas SSH:
git remote add origin git@github.com:TU_USUARIO/mi-proyecto-udemy.git

# Subir el proyecto
git push -u origin main
```

> La URL exacta te la da GitHub en la página del repositorio vacío que creaste.

La opción `-u` en el push establece el *upstream tracking* — después solo necesitarás escribir `git push` y `git pull`.

---

## FASE 5 — Clonar el proyecto en el Ordenador 2

En el segundo ordenador **no** hagas `git init`. En su lugar, clona directamente:

```bash
cd /ruta/donde/quieres/el/proyecto

# HTTPS:
git clone https://github.com/TU_USUARIO/mi-proyecto-udemy.git

# SSH:
git clone git@github.com:TU_USUARIO/mi-proyecto-udemy.git
```

Esto crea la carpeta del proyecto, descarga todo el código y ya configura el remote `origin` automáticamente.

Luego recrea el entorno virtual con **uv**:

```bash
cd mi-proyecto-udemy
uv sync        # recrea .venv e instala dependencias desde pyproject.toml / uv.lock
```

**Qué hace exactamente `uv sync`:**

- Crea `.venv` si no existe
- Instala todas las dependencias de `pyproject.toml`
- Si existe `uv.lock`, respeta las versiones exactas pinneadas (reproducibilidad garantizada)
- Si no existe `uv.lock`, resuelve y genera uno nuevo

**Variantes útiles:**

```bash
# Incluir también dependencias de desarrollo (grupos opcionales)
uv sync --all-extras

# Solo un grupo concreto definido en pyproject.toml
uv sync --extra dev

# Forzar reinstalación aunque ya exista el entorno
uv sync --reinstall
```

**Para activar el entorno después:**

```bash
# Linux/macOS
source .venv/bin/activate

# Windows CMD
.venv\Scripts\activate.bat

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

O simplemente usar `uv run <script.py>` directamente sin activar, que es el flujo más limpio con `uv`.

---

## FASE 6 — Flujo de trabajo diario en VSCode

VSCode tiene integración Git nativa (panel *Source Control*, icono de rama en la barra lateral). Puedes hacer todo desde la UI, pero te recomiendo aprender los comandos primero:

### Al empezar a trabajar (en cualquier ordenador):
```bash
git pull
```

### Al terminar de trabajar:
```bash
git add .
git commit -m "Descripción de lo que hiciste"
git push
```

### Regla de oro para evitar conflictos:
> **Siempre haz `pull` antes de ponerte a trabajar** y **`push` antes de cerrar el ordenador.**

---

## Resumen visual del flujo

```
Ordenador 1  ──push──▶  GitHub  ◀──clone──  Ordenador 2
     ▲                     │                     │
     └──────────pull───────┘         pull/push ──┘
```

---

## Checklist rápido

- [ ] Git instalado y `user.name` / `user.email` configurados en ambos ordenadores
- [ ] Repositorio vacío creado en GitHub
- [ ] Token o clave SSH configurada en ambos ordenadores
- [ ] `git push -u origin main` ejecutado desde el Ordenador 1
- [ ] `git clone ...` ejecutado en el Ordenador 2
- [ ] `uv sync` para recrear `.venv` en el Ordenador 2


---

## VSCode y las operaciones Git

**VSCode reconoce todo automáticamente.** Cuando abres una carpeta que tiene `.git/`, VSCode activa el panel *Source Control* y ya puede hacer add/commit/pull/push sin tocar el terminal. Funciona así:

- **Las credenciales** las gestiona GCM a nivel de sistema — VSCode las usa de forma transparente, no necesita configuración adicional.
- **El ejecutable de Git** lo detecta VSCode automáticamente si está en el PATH (Git Bash lo añade al PATH de Windows durante la instalación).

### Operaciones desde VSCode

| Operación | Dónde está en VSCode |
|---|---|
| `git add` | Panel Source Control → icono `+` junto al archivo, o *Stage All Changes* |
| `git commit` | Cuadro de texto del mensaje → botón **Commit** |
| `git push` | Botón **Sync Changes** (push+pull combinado) o menú `···` → *Push* |
| `git pull` | Menú `···` → *Pull*, o botón **Sync Changes** |

El botón **Sync Changes** que aparece en la barra de estado inferior (con el icono de flechas circulares) hace `pull` + `push` en una sola acción, que es lo más cómodo para el flujo diario.


### Una recomendación adicional para VSCode

Instala la extensión **GitLens** — no es imprescindible pero añade historial inline, comparación de ramas y visualización de blame que resulta muy útil mientras aprendes Git. Es gratuita.