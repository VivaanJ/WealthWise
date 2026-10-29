# WealthWise — Enhanced UML Diagrams & Code Walkthrough

This is a GitHub-rendered visual appendix for the WealthWise academic project. It explains the five UML views and links each diagram to the actual Java/browser code. It is a companion reference to the full Word report.

> **Important implementation boundary:** index.html is the browser-based application. WealthWise.java is a separate Java console companion. They are not connected and do not share state. Prices and balances are simulated.

## 1. Use Case Diagram — What the user can do

~~~mermaid
flowchart LR
    actor([Investor / Student])
    subgraph WW[WealthWise Simulation]
        U1([View dashboard])
        U2([Browse sample assets])
        U3([Buy virtual units])
        U4([Sell virtual units])
        U5([Review portfolio])
        U6([View transaction history])
        U7([Export CSV])
        U8([Reset simulation])
    end
    actor --- U1
    actor --- U2
    actor --- U3
    actor --- U4
    actor --- U5
    actor --- U6
    actor --- U7
    actor --- U8
~~~

**How to read it:** the actor is the student/investor. Each oval is a user goal or feature. It describes what the system lets the user do, not the internal order of code execution.

## 2. Class Diagram — How the Java code is organised

~~~mermaid
classDiagram
    class WealthWise {
      -Portfolio portfolio
      -List~Asset~ market
      +main(String[] args)
      -showDashboard()
      -buyAsset()
      -sellAsset()
    }
    class Asset {
      <<abstract>>
      -String symbol
      -String name
      -double price
      +getSymbol()
      +getName()
      +getPrice()
      +getCategory()
      +getDescription()
    }
    class Stock {
      +getCategory()
      +getDescription()
    }
    class MutualFund {
      +getCategory()
      +getDescription()
    }
    class Portfolio {
      -double cash
      -double realizedProfitLoss
      -Map holdings
      -List transactions
      +buy(Asset, int)
      +sell(Asset, int)
      +getTotalValue(List)
      +getCombinedProfitLoss(List)
    }
    class Holding {
      -int units
      -double averageBuyPrice
      +addUnits(int, double)
      +removeUnits(int)
    }
    class Transaction {
      -String action
      -Asset asset
      -int units
      -double unitPrice
      -double amount
      -double profitLoss
    }
    Asset <|-- Stock : inherits
    Asset <|-- MutualFund : inherits
    WealthWise --> Asset : market list
    WealthWise --> Portfolio : uses
    Portfolio "1" *-- "0..*" Holding : manages
    Portfolio "1" *-- "0..*" Transaction : records
    Transaction --> Asset : refers to
~~~

**How to read it:** the hollow triangle means inheritance. Stock and MutualFund are specialised Asset types. The filled diamond shows that Portfolio manages its holdings and transaction records. The Java implementation uses nested classes, but they are drawn separately here to make responsibilities easier to read.

### Code snippet: abstraction and inheritance

From WealthWise.java:

~~~java
private static abstract class Asset {
    private final String symbol;
    private final String name;
    private double price;

    public abstract String getCategory();
    public abstract String getDescription();
}

private static class Stock extends Asset {
    @Override
    public String getCategory() {
        return "Stock";
    }
}

private static class MutualFund extends Asset {
    @Override
    public String getCategory() {
        return "Mutual Fund";
    }
}
~~~

**What it proves:** Asset defines what all assets share. The child classes inherit that shared structure and provide type-specific behaviour.

## 3. Sequence Diagram — What happens during a buy

~~~mermaid
sequenceDiagram
    actor Investor
    participant App as WealthWise
    participant P as Portfolio
    participant H as Holding
    participant T as Transaction

    Investor->>App: Select asset and quantity
    App->>P: buy(asset, units)
    P->>P: Check units > 0
    P->>P: Check available cash
    alt valid quantity and sufficient cash
        P->>H: Create holding or add units
        P->>P: Deduct purchase amount from cash
        P->>T: Record BUY transaction
        P-->>App: Purchase completed
        App-->>Investor: Display updated portfolio
    else invalid input or insufficient cash
        P-->>App: Raise validation error
        App-->>Investor: Show rejection message
    end
~~~

**How to read it:** time flows from top to bottom. Each arrow is a message or method call. It shows which participant communicates with another and in what order.

### Code snippet: buy validation and update

From WealthWise.java:

~~~java
public void buy(Asset asset, int units) {
    if (units <= 0) {
        throw new IllegalArgumentException("Units must be positive.");
    }

    double amount = asset.getPrice() * units;
    if (amount > cash) {
        throw new IllegalArgumentException("Insufficient cash.");
    }

    Holding holding = holdings.get(asset.getSymbol());
    if (holding == null) {
        holdings.put(asset.getSymbol(),
            new Holding(units, asset.getPrice()));
    } else {
        holding.addUnits(units, asset.getPrice());
    }

    cash -= amount;
    transactions.add(new Transaction(
        "BUY", asset, units, asset.getPrice(), amount, 0));
}
~~~

**What it proves:** the program checks quantity and cash before modifying the portfolio, updates or creates the holding, deducts cash and records the transaction.

## 4. Activity Diagram — The decision flow of buying

~~~mermaid
flowchart TD
    A([Start]) --> B[User selects asset and quantity]
    B --> C{Quantity is positive?}
    C -- No --> X[Reject trade and show message]
    C -- Yes --> D[Calculate price × quantity]
    D --> E{Enough virtual cash?}
    E -- No --> X
    E -- Yes --> F[Create or update holding]
    F --> G[Deduct cash]
    G --> H[Record transaction]
    H --> I[Refresh portfolio totals]
    I --> J([End])
    X --> J
~~~

**How to read it:** diamonds are decisions; arrows show which path is taken. This diagram focuses on the process and its branching rules. It differs from the sequence diagram, which focuses on messages passed between objects.

### Code snippet: validation when selling

From WealthWise.java:

~~~java
Holding holding = holdings.get(asset.getSymbol());
if (holding == null || units <= 0
        || units > holding.getUnits()) {
    throw new IllegalArgumentException(
        "Not enough units to sell.");
}
~~~

**What it proves:** the program rejects a sale when the user has no holding, the requested quantity is not positive, or the user tries to sell more units than they own.

## 5. Component / Deployment Diagram — Where the parts run

~~~mermaid
flowchart TB
    subgraph Browser["Browser environment"]
        UI["index.html<br/>HTML + CSS + JavaScript"]
        LS[("localStorage<br/>saved browser simulation state")]
        UI <--> LS
    end

    subgraph Java["Java runtime"]
        CLI["WealthWise.java<br/>console menu"]
        MODEL["Asset / Stock / MutualFund<br/>Portfolio / Holding / Transaction"]
        CLI --> MODEL
    end

    UI -.- N["No API or shared-state connection"]
    N -.- CLI
~~~

**How to read it:** the browser application stores its own state in browser localStorage. The Java application holds data in Java objects while it runs. The dotted connector is explicitly a note that the two applications are separate, not a data connection.

### Code snippet: local browser persistence

From index.html:

~~~javascript
const STORAGE_KEY = "wealthwise-web-v1";

function persist() {
  try {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify(state)
    );
  } catch (e) {
    toast("Could not save data in this browser.");
  }
}
~~~

**What it proves:** browser state is saved locally using localStorage. That is independent of the Java console program.

## 6. One small worked example

Suppose the initial virtual cash is ₹100,000 and a student buys 2 TCS units at the illustrative price of ₹3,850 each.

| Measure | Before | After purchase |
|---|---:|---:|
| Available cash | ₹100,000 | ₹92,300 |
| TCS units held | 0 | 2 |
| Purchase cost | ₹0 | ₹7,700 |
| TCS market value at unchanged price | ₹0 | ₹7,700 |
| Total portfolio value | ₹100,000 | ₹100,000 |

If the simulated price later rises to ₹3,900, then market value is 2 × ₹3,900 = ₹7,800 and unrealized profit is ₹7,800 − ₹7,700 = ₹100. This is a virtual example, not a live quote.

## 7. Five diagrams in one line

| Diagram | Main question it answers |
|---|---|
| Use Case | What can the user do? |
| Class | Which classes exist, and how are they related? |
| Sequence | Which objects communicate, and in what order? |
| Activity | What steps and decisions happen in a process? |
| Component / Deployment | What are the main parts, and where do they run? |

## Source files

- [Java source](WealthWise.java)
- [Browser application](index.html)
- [UML design PDF](WealthWise_UML_Design_Document.pdf)

