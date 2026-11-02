# portifolio

Site pessoal de Dyego Seabra, no ar em https://dyegoseabra.com.br.

Página estática, sem build: `index.html` com CSS e JavaScript embutidos, alternância PT/EN e os currículos em `assets/`.

## Deploy

O site é servido pelo nginx da VPS em `/var/www/portfolio`. Depois de editar:

```bash
rsync -a --delete --exclude '.git' --exclude 'README.md' ./ LPD:/var/www/portfolio/
ssh LPD 'chown -R www-data:www-data /var/www/portfolio'
```
