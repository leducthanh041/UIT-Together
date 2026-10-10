# Bootstrap portfolio redesign

## Objective
Follow the provided Bootstrap-5-portfolio-template composition: gradient navigation and split hero, wave divider, rounded arrow buttons, illustrated alternating sections, centered section headings and a dark footer. Adapt the palette to UIT blue and use real group content.

## Implementation
1. Audit the template and existing routes; preserve publications, author order, contacts and all public URLs.
2. Vendor Bootstrap 5.0.2 from the template locally, retain its license header, recolor brand tokens; remove Bootstrap 3 and the old lab theme from the active layout. Keep compatibility styles for historic content. Copy only necessary illustrations and Font Awesome assets. No external font or CDN requests.
3. Create a blue gradient header and two-column home hero with a large UIT Together wordmark, Computer Vision / Machine Learning, template illustration, arrow CTAs and the original wave shape.
4. Add concise research sections with alternating illustrations and an actual team photograph. Keep scrollable Group updates and Publication highlights, DOI links and the existing directory.
5. Apply shared typography, controls and footer to Research, People, Publications, Datasets, Tutorials and Contact. Keep accessible mobile navigation, keyboard focus, reduced motion, scroll reveal and bounded subpage scrolling.
6. Build using Conda UITweb, run route/asset checks, Python data/route tests, JS filtering checks and whitespace validation. Document any unavailable browser validation.

## Content boundaries
Do not copy demo clients, testimonials, statistics, phone numbers, social links or nonfunctional contact forms. Keep only verified contact emails. /homes/ and /PapersByYear/ remain compatibility redirects. No public deployment or package installation is required.

## Asset provenance
Template author: Patrick Muriungi; package.json declares ISC. Bootstrap 5.0.2 retains its MIT banner; Font Awesome retains upstream license notices. Illustrations are copied from the user-provided template, displayed decoratively, and recolored through CSS. Confirm illustration redistribution rights before public deployment.

## Verification result
Implemented in src/layouts/base.html, shared header/footer, home-content.html and assets/css/portfolio.css. Build generated 145 pages. All five Python tests and the JavaScript publication filter tests passed. Asset/route checker found zero new missing links; 123 historic missing links remain in the baseline. JavaScript syntax and git diff whitespace checks passed. No browser automation is available in this agent environment, so actual desktop/mobile rendering still needs a browser review.
