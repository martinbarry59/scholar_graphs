
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/martinbarry59/scholar_graphs">
<!--     <img src="images/logo.png" alt="Logo" width="80" height="80"> -->
  </a>

  <h3 align="center">Scholar Graphs</h3>

  <p align="center">
    A  simple model for plotting connectivity between authors!
    <br />
    <a href="https://github.com/martinbarry59/scholar_graphs"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    ·
    <a href="https://github.com/martinbarry59/scholar_graphs/issues">Report Bug</a>
    ·
    <a href="https://github.com/martinbarry59/scholar_graphs/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This code is a very simple and easy-to-use scraper of profiles and graph generator (maybe papers in the future but right now Google scholar blocks connections for querys...).

<!-- GETTING STARTED -->
## Getting Started

The code uses python 3. use the following to download the required libraries

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```
   pip install -r requirements.txt
  ```

<!-- USAGE EXAMPLES -->
## Usage

Run the script: scrape_profiles.py to scrape the coauthors up to a given number of node distances starting from an initial author

e.g run
 ```
  python scrape_profiles.py --name 'Martin Barry' --depth 3

  ```


Run the script: make_graph.py to simply create the matrix of connectivity between authors. This matrix can then be plotted using [Gephi](https://gephi.org/)
e.g run
 ```
  python make_graph.py  --depth 3

  ```

<!-- CONTRIBUTING -->
## Contributing
 Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request




<!-- CONTACT -->
## Contact

Project Link: [https://github.com/martinbarry59/scholar_graphs](https://github.com/martinbarry59/scholar_graphs)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://shields.io)
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Pages](https://pages.github.com)
* [Animate.css](https://daneden.github.io/animate.css)
* [Loaders.css](https://connoratherton.com/loaders)
* [Slick Carousel](https://kenwheeler.github.io/slick)
* [Smooth Scroll](https://github.com/cferdinandi/smooth-scroll)
* [Sticky Kit](http://leafo.net/sticky-kit)
* [JVectorMap](http://jvectormap.com)
* [Font Awesome](https://fontawesome.com)

