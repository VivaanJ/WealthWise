# WealthWise — Virtual Investment & Portfolio Simulator

An academic OOP project for NMIMS MBA Tech AI. WealthWise is an educational simulation for practicing portfolio operations with virtual money. It does not connect to a broker, place real trades, or use live market prices.

## Contents
- [index.html](index.html) — self-contained browser simulation (HTML/CSS/JavaScript)
- [WealthWise.java](WealthWise.java) — standalone Java console companion demonstrating OOP
- [WealthWise_UML_Design_Document.pdf](WealthWise_UML_Design_Document.pdf) — use case, class, sequence, activity, and component/deployment views

## Run the web simulation
Open index.html in a modern desktop browser. No server or Java runtime is required for the browser version. It starts with ₹100,000 virtual cash and uses illustrative sample assets/prices.

## Compile and run the Java program
With a Java Development Kit installed:

```bash
javac WealthWise.java
java WealthWise
```

The Java console app is a separate implementation and does not power or synchronize with the web page.

## OOP concepts demonstrated
- **Abstraction:** abstract `Asset` defines the common asset model.
- **Inheritance:** `Stock` and `MutualFund` extend `Asset`.
- **Polymorphism:** overridden asset methods are called through `Asset` references.
- **Encapsulation:** private fields and controlled methods guard portfolio state.
- **Composition:** `Portfolio` manages holdings and transaction records.

## Project links
- Repository: https://github.com/VivaanJ/WealthWise
- Java source: https://github.com/VivaanJ/WealthWise/blob/main/WealthWise.java
- UML PDF: https://github.com/VivaanJ/WealthWise/blob/main/WealthWise_UML_Design_Document.pdf

## Disclaimer
For academic learning only. All amounts and prices are virtual/sample values; this project is not investment advice or a trading platform.
