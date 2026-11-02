# portifolio

Site pessoal de Dyego Seabra, no ar em https://dyegoseabra.com.br.

Página estática, sem build: `index.html` com CSS e JavaScript embutidos, alternância PT/EN e os currículos em `assets/`.

## Deploy

O site é servido pelo nginx da VPS em `/var/www/portfolio`. Depois de editar:

```bash
rsync -a --delete --exclude '.git' --exclude 'README.md' --exclude 'scripts' ./ LPD:/var/www/portfolio/
ssh LPD 'chown -R www-data:www-data /var/www/portfolio'
```

## SEO e LLMs

- `<head>` com descrição, canonical, Open Graph e Twitter (imagem em `assets/og-image.jpg`, 1200×630) e JSON-LD (`Person`, `WebSite`, `ProfilePage` e um `CreativeWork` por projeto). Fato novo no site entra também no JSON-LD
- `robots.txt` libera buscadores e assistentes de IA; `sitemap.xml` lista a página, as imagens e os currículos. Atualize o `lastmod` quando mudar o conteúdo
- `llms.txt` é o resumo à mão para LLMs. `llms-full.txt` é gerado do HTML; depois de editar o site, rode:

```bash
python3 -I scripts/llms_full.py .
```
