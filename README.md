# Study of Nature

This is the main repository for my statically generated website hosted at https://blog.joey-dumont.ca. It is a Jekyll-based site, using a  (now very dated) [fork](https://github.com/joeydumont/so-simple-theme) of the [So Simple theme](https://github.com/mmistakes/so-simple-theme).

## Generating the website

I have split the git repository in two diverging branches, source and master. While they are indeed git branches, they are not meant to ever be merged back together. The source branch contains the Markdown, CSS, and HTML templates used to generate the site, and the master branch contains the results of the static generation.

I typically keep two copies of the repository on my machine, one at `SoN.source` and the other at `SoN.content`. The `deploy.sh` script simply writes the results to `SoN.content`.

While I have been generally satisfied with Jekyll, I have found dependency management to be a monumental pain. Arch Linux typically has the very latest ruby version, and doesn't seem to always play well with `bundle`.  I typically generate the website using `apptainer` and the latest ruby image.

```bash
apptainer pull docker://ruby:latest
apptainer exec ruby_latest.sif /bin/bash
bundle update

# To see drafts locally
Apptainer> bundle exec jekyll  serve --drafts

# To deploy
Apptainer > ./deploy.sh
```
Using apptainer is pretty convenient, as it bind mounts your current working directory by default, making the site files available inside the container.

Then, push both the source files and the generated files to GitHub.
  - [ ] TODO: Automate this with github-ci.

## Changing the syntax highlighter style

I am currently using `rouge` as the syntax highlighter (not sure there's really another way in Jekyll). Use this to update the theme
```bash
bundle exec rougify style base16.solarized > _sass/_syntax.scss
```

See [this page](https://github.com/mzlogin/rouge-themes) for a list of themes to choose from.

## Maintenance

There a couple aspects of the statically generated website that need to be updated on a regular basis.

### Ruby Gems

```bash
apptainer pull docker://ruby:latest
apptainer exec ruby_latest.sif /bin/bash
bundle update
```

### jQuery

Update [scripts.html](_includes/scripts.html) to pull in the latest version of jQuery.
