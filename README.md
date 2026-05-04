# Fractal Semantic Encoding (FSE)
## *Biomemetic Data Architecture for Exact Query Processing (EQP)*

[![License: Apache 2.0](https://img.shields.io/badge/Code_License-Apache_2.0-blue.svg)](LICENSE)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/Paper_License-CC_BY--NC--ND_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)

## Background
Since October 2025, I've been heads-down on this project. To be blunt: unemployment gave me a massive surplus of probably the most valuable resource in engineering: **uninterrupted time.** The actual catalyst for this project came from a different, far more frustrating resource problem. A piece of me dies everytime I get an email saying my Google Drive is full or a notification saying that my iCloud is at max capacity. How do you solve this? You either pay for more storage or you just make a new account.

You know what else is really absurd? It's the tech industry's macro-level solution to this exact problem: "Oh hey we, ran out of space? Let's erect a giant concrete structure to house more raw disk." We are laying down millions of square feet of data centers, draining local power grids, and burning gigawatts of energy just to warehouse passive, bloated data. We keep throwing physical hardware at a software problem, paying for more passive space instead of making the storage layer itself smarter.

Indeed, I am active in my job search. Instead of treating my job search as a waiting room, I wanted to dedicate this time to deep dive into research and applied engineering. Honestly if I had the means to go back to grad school to research what I'm about to disclose here, I would've loved to. But alas, Columbia is expensive and my wallet is very, very fragile.

Since I currently can't afford a master's degree, I essentially built my own curriculum. My syllabus comprised of understanding the exact points of architectural rigidity in modern systems, why schema migrations cause so much downtime, and why data cleaning is such a nightmare. Once the constraints were revealed to me, I realized traditional RDBMS logic is not enough. Databases are dumb filing cabinets; they rigidly store massive volumes of flat data until they collapse under their own weight. Let's move away from the rigid constraints of the computer world for a second. What's the most efficient information processing engine in existence?

**THE BRAIN**

Funny enough, the inspiration to figure out how nature handles high-density data storage came to me while I was watching *Pantheon.* But where the show leans into the sci-fi whimsy of uploading a 1:1 human consiousness (the "Uploaded Intelligence" as they called it), I wanted to obviously strip that idea down to its most grounded, realistic foundation. That being said, I want to be explicitly clear: I have zero interest in turning this into another "breakthrough" in the Generative AI hype cycle. In the context of data architecture, trying to use LLMs to manage structured information is doomed to fail. You cannot build a reliable foundation on a probablistic black box that hallucinates facts and burns enough electricity to power a small city just to run the world's most expensive game of autocorrect.

**FSE is built to mimic the brain's structural efficiency, not its imagination.** I don't want probablistic guesses; I want the mathematical certainty of Exact Query Processing (you can read more baout this in my white-paper or in the wiki).

Biological brains don't log raw data rows; they filter noise and map inputs into repeating semantic patterns. This fact led me to ask: *"What is the mathematical equivalent of organic pattern recognition?"* This question pulled me completely out of database architectures. If you want to mathematically model how nature organizes compelx, self-similar structures, you use fractal geometry. If you want to model how a system filters noise to isolate meaningful changes, you use signal processing and wave mathematics. By smashing modern data frustration and the mathematics of biomimicry, the concept became clear: instead of storing data as passive rows, what if we start storing it as an active, self-organizing geometric model?

<details>
<summary><strong> Click here to view my research log/inspirations </strong></summary>

### **1. Identifying the Structural Rot**
*Before I could even build a solution, I had to quantify exactly why modern data infrastructure is failing. I spent some weeks dissecting the failure points of modern data infrastructure. I went over various sources, but I ultimately landed on these to build the framework for the "problem space" FSE is designed to solve:*

* **Zhamak Dehghani: Data Mesh (2022)** - This was my primary source for **Tier 1 (Deterministic Walls).** Dehghani proved that centralized data lakes are a bottlebeck; data needs to be categorized locally to avoid **architectural bloat.**

</details>