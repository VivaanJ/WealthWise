import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

/**
 * WealthWise - Virtual Investment Simulator
 * Single-file Java OOP lab project.
 *
 * Demonstrates:
 * 1. Encapsulation: private fields and controlled methods
 * 2. Inheritance: Stock and MutualFund extend Asset
 * 3. Abstraction: Asset is an abstract class
 * 4. Polymorphism: overridden getCategory()/getDescription() methods
 *
 * All money and prices are virtual. No real trades or live market data are used.
 * Compile: javac WealthWise.java
 * Run:     java WealthWise
 */
public class WealthWise {
    private static final Scanner INPUT = new Scanner(System.in);
    private static final double STARTING_CASH = 100000.00;
    private static final DateTimeFormatter DATE_FORMAT =
            DateTimeFormatter.ofPattern("dd MMM yyyy, hh:mm a");

    private final Portfolio portfolio = new Portfolio(STARTING_CASH);
    private final List<Asset> market = new ArrayList<Asset>();
    private final Random random = new Random();

    public WealthWise() {
        market.add(new Stock("TCS", "Tata Consultancy Services", 3850.00));
        market.add(new Stock("INFY", "Infosys", 1750.00));
        market.add(new Stock("RELIANCE", "Reliance Industries", 2900.00));
        market.add(new MutualFund("NIFTY50", "Nifty 50 Index Fund", 250.00));
        market.add(new MutualFund("BLUECHIP", "Bluechip Fund", 180.00));
    }

    public static void main(String[] args) {
        new WealthWise().run();
    }

    private void run() {
        System.out.println("\n==========================================");
        System.out.println("       WEALTHWISE INVESTMENT SIMULATOR");
        System.out.println("==========================================");
        System.out.println("Practice investing with virtual money only.");
        boolean running = true;

        while (running) {
            printMenu();
            int choice = readInt("Choose an option: ");
            switch (choice) {
                case 1: showDashboard(); break;
                case 2: showMarket(); break;
                case 3: buyAsset(); break;
                case 4: sellAsset(); break;
                case 5: showPortfolio(); break;
                case 6: simulateMarketMovement(); break;
                case 7: showTransactions(); break;
                case 8: resetDemo(); break;
                case 0:
                    running = false;
                    System.out.println("Thank you for using WealthWise. Goodbye!");
                    break;
                default:
                    System.out.println("Please choose a number from 0 to 8.");
            }
        }
        INPUT.close();
    }

    private void printMenu() {
        System.out.println("\n--------------- MAIN MENU ---------------");
        System.out.println("1. Dashboard");
        System.out.println("2. Market watch");
        System.out.println("3. Buy asset");
        System.out.println("4. Sell asset");
        System.out.println("5. My portfolio");
        System.out.println("6. Simulate market movement");
        System.out.println("7. Transaction history");
        System.out.println("8. Reset demo");
        System.out.println("0. Exit");
        System.out.println("------------------------------------------");
        System.out.printf("Available cash: %s%n", money(portfolio.getCash()));
    }

    private void showDashboard() {
        double investmentValue = portfolio.getInvestmentValue(market);
        double totalValue = portfolio.getTotalValue(market);
        double profitLoss = portfolio.getCombinedProfitLoss(market);
        double returnPercent = (totalValue - STARTING_CASH) / STARTING_CASH * 100.0;

        System.out.println("\n============== DASHBOARD =================");
        System.out.println("Available cash       : " + money(portfolio.getCash()));
        System.out.println("Investment value     : " + money(investmentValue));
        System.out.println("Total portfolio      : " + money(totalValue));
        System.out.println("Combined profit/loss : " + signedMoney(profitLoss));
        System.out.printf("Return on start      : %.2f%%%n", returnPercent);
        System.out.println("Completed trades     : " + portfolio.getTradeCount());
        System.out.println("==========================================");
    }

    private void showMarket() {
        System.out.println("\n================ MARKET ==================");
        System.out.printf("%-10s %-31s %-14s %12s%n",
                "SYMBOL", "ASSET", "TYPE", "PRICE");
        System.out.println("--------------------------------------------------------------------------");
        for (Asset asset : market) {
            // Polymorphism: each asset supplies its own category/description.
            System.out.printf("%-10s %-31s %-14s %12s%n",
                    asset.getSymbol(), shorten(asset.getName(), 30),
                    asset.getCategory(), money(asset.getPrice()));
        }
        System.out.println("Prices are sample values, not live market prices.");
    }

    private void buyAsset() {
        Asset asset = chooseAsset();
        if (asset == null) return;

        int units = readInt("Enter quantity to buy (whole units): ");
        if (units <= 0) {
            System.out.println("Quantity must be greater than zero.");
            return;
        }

        double amount = asset.getPrice() * units;
        if (amount > portfolio.getCash()) {
            System.out.println("Insufficient cash. Required " + money(amount)
                    + ", available " + money(portfolio.getCash()) + ".");
            return;
        }

        portfolio.buy(asset, units);
        System.out.println("Purchase successful: " + units + " unit(s) of "
                + asset.getSymbol() + " for " + money(amount) + ".");
    }

    private void sellAsset() {
        if (portfolio.getHoldings().isEmpty()) {
            System.out.println("You do not own any assets yet.");
            return;
        }

        showPortfolioHoldings();
        String symbol = readText("Enter symbol to sell: ").toUpperCase(Locale.ROOT);
        Asset asset = findAsset(symbol);
        Holding holding = portfolio.getHolding(symbol);

        if (asset == null || holding == null) {
            System.out.println("That asset is not in your portfolio.");
            return;
        }

        int units = readInt("Enter quantity to sell (you own "
                + holding.getUnits() + "): ");
        if (units <= 0 || units > holding.getUnits()) {
            System.out.println("Enter a quantity from 1 to " + holding.getUnits() + ".");
            return;
        }

        double proceeds = asset.getPrice() * units;
        double profitLoss = (asset.getPrice() - holding.getAverageBuyPrice()) * units;
        portfolio.sell(asset, units);
        System.out.println("Sale successful: " + units + " unit(s) of "
                + asset.getSymbol() + " for " + money(proceeds) + ".");
        System.out.println("Realized profit/loss: " + signedMoney(profitLoss));
    }

    private void showPortfolio() {
        System.out.println("\n============== MY PORTFOLIO ==============");
        System.out.println("Cash balance         : " + money(portfolio.getCash()));
        System.out.println("Invested cost        : " + money(portfolio.getInvestedCost()));
        System.out.println("Investment value     : " + money(portfolio.getInvestmentValue(market)));
        System.out.println("Unrealized P/L       : " + signedMoney(portfolio.getUnrealizedProfitLoss(market)));
        System.out.println("Realized P/L         : " + signedMoney(portfolio.getRealizedProfitLoss()));
        System.out.println("Total portfolio      : " + money(portfolio.getTotalValue(market)));
        System.out.println("Combined P/L         : " + signedMoney(portfolio.getCombinedProfitLoss(market)));
        showPortfolioHoldings();
    }

    private void showPortfolioHoldings() {
        System.out.println("\nHoldings:");
        if (portfolio.getHoldings().isEmpty()) {
            System.out.println("  No holdings yet. Buy an asset to get started.");
            return;
        }

        System.out.printf("%-10s %7s %14s %14s %14s %14s%n",
                "SYMBOL", "UNITS", "AVG BUY", "PRICE", "VALUE", "UNREAL. P/L");
        System.out.println("-------------------------------------------------------------------------------");

        for (Map.Entry<String, Holding> entry : portfolio.getHoldings().entrySet()) {
            Asset asset = findAsset(entry.getKey());
            Holding holding = entry.getValue();
            double value = asset.getPrice() * holding.getUnits();
            double pl = (asset.getPrice() - holding.getAverageBuyPrice()) * holding.getUnits();
            System.out.printf("%-10s %7d %14s %14s %14s %14s%n",
                    asset.getSymbol(), holding.getUnits(),
                    money(holding.getAverageBuyPrice()), money(asset.getPrice()),
                    money(value), signedMoney(pl));
        }
    }

    private void simulateMarketMovement() {
        System.out.println("\nSimulating market movement...");
        for (Asset asset : market) {
            double changePercent = -5.0 + random.nextDouble() * 10.0;
            double newPrice = Math.max(0.01, asset.getPrice() * (1.0 + changePercent / 100.0));
            asset.updatePrice(newPrice);
            System.out.printf("%-10s %s (%+.2f%%)%n", asset.getSymbol(),
                    money(asset.getPrice()), changePercent);
        }
        portfolio.recordMarketUpdate();
        System.out.println("Market movement complete. Portfolio values have been updated.");
    }

    private void showTransactions() {
        System.out.println("\n============= TRANSACTION HISTORY =========");
        List<Transaction> history = portfolio.getTransactions();
        if (history.isEmpty()) {
            System.out.println("No transactions recorded yet.");
            return;
        }

        for (Transaction transaction : history) {
            System.out.println(transaction);
        }
    }

    private void resetDemo() {
        String answer = readText("Reset cash, holdings and history? (yes/no): ");
        if (!"yes".equalsIgnoreCase(answer)) {
            System.out.println("Reset cancelled.");
            return;
        }
        portfolio.reset(STARTING_CASH);
        market.get(0).updatePrice(3850.00);
        market.get(1).updatePrice(1750.00);
        market.get(2).updatePrice(2900.00);
        market.get(3).updatePrice(250.00);
        market.get(4).updatePrice(180.00);
        System.out.println("Demo reset. Starting cash is " + money(STARTING_CASH) + ".");
    }

    private Asset chooseAsset() {
        showMarket();
        String symbol = readText("Enter asset symbol: ").toUpperCase(Locale.ROOT);
        Asset asset = findAsset(symbol);
        if (asset == null) {
            System.out.println("Unknown symbol. Please select one from the market list.");
        }
        return asset;
    }

    private Asset findAsset(String symbol) {
        for (Asset asset : market) {
            if (asset.getSymbol().equalsIgnoreCase(symbol)) return asset;
        }
        return null;
    }

    private int readInt(String prompt) {
        while (true) {
            System.out.print(prompt);
            String value = INPUT.nextLine().trim();
            try {
                return Integer.parseInt(value);
            } catch (NumberFormatException ex) {
                System.out.println("Please enter a valid whole number.");
            }
        }
    }

    private String readText(String prompt) {
        System.out.print(prompt);
        return INPUT.nextLine().trim();
    }

    private static String money(double amount) {
        return String.format(Locale.US, "₹%,.2f", amount);
    }

    private static String signedMoney(double amount) {
        return (amount >= 0 ? "+" : "-") + money(Math.abs(amount));
    }

    private static String shorten(String text, int maxLength) {
        return text.length() <= maxLength ? text : text.substring(0, maxLength - 3) + "...";
    }

    // ---------------------- ABSTRACTION ----------------------
    // Asset defines common data/behaviour but cannot be instantiated directly.
    private static abstract class Asset {
        private final String symbol;
        private final String name;
        private double price;

        protected Asset(String symbol, String name, double price) {
            this.symbol = symbol;
            this.name = name;
            this.price = price;
        }

        public String getSymbol() { return symbol; }
        public String getName() { return name; }
        public double getPrice() { return price; }

        public void updatePrice(double newPrice) {
            if (newPrice <= 0) throw new IllegalArgumentException("Price must be positive.");
            this.price = newPrice;
        }

        public abstract String getCategory();
        public abstract String getDescription();
    }

    // ---------------------- INHERITANCE ----------------------
    private static class Stock extends Asset {
        public Stock(String symbol, String name, double price) {
            super(symbol, name, price);
        }

        @Override
        public String getCategory() { return "Stock"; }

        @Override
        public String getDescription() {
            return getName() + " is a simulated company share.";
        }
    }

    private static class MutualFund extends Asset {
        public MutualFund(String symbol, String name, double price) {
            super(symbol, name, price);
        }

        @Override
        public String getCategory() { return "Mutual Fund"; }

        @Override
        public String getDescription() {
            return getName() + " is a simulated pooled investment fund.";
        }
    }

    // ---------------------- ENCAPSULATION ----------------------
    private static class Holding {
        private int units;
        private double averageBuyPrice;

        public Holding(int units, double averageBuyPrice) {
            this.units = units;
            this.averageBuyPrice = averageBuyPrice;
        }

        public int getUnits() { return units; }
        public double getAverageBuyPrice() { return averageBuyPrice; }

        public void addUnits(int additionalUnits, double purchasePrice) {
            double totalCost = averageBuyPrice * units + purchasePrice * additionalUnits;
            units += additionalUnits;
            averageBuyPrice = totalCost / units;
        }

        public void removeUnits(int soldUnits) {
            if (soldUnits <= 0 || soldUnits > units) {
                throw new IllegalArgumentException("Invalid quantity to sell.");
            }
            units -= soldUnits;
        }
    }

    private static class Portfolio {
        private double cash;
        private double realizedProfitLoss;
        private final Map<String, Holding> holdings = new LinkedHashMap<String, Holding>();
        private final List<Transaction> transactions = new ArrayList<Transaction>();

        public Portfolio(double startingCash) {
            cash = startingCash;
        }

        public double getCash() { return cash; }
        public double getRealizedProfitLoss() { return realizedProfitLoss; }
        public Map<String, Holding> getHoldings() {
            return Collections.unmodifiableMap(holdings);
        }
        public Holding getHolding(String symbol) { return holdings.get(symbol); }
        public List<Transaction> getTransactions() {
            return Collections.unmodifiableList(transactions);
        }

        public void buy(Asset asset, int units) {
            if (units <= 0) throw new IllegalArgumentException("Units must be positive.");
            double amount = asset.getPrice() * units;
            if (amount > cash) throw new IllegalArgumentException("Insufficient cash.");

            Holding holding = holdings.get(asset.getSymbol());
            if (holding == null) {
                holdings.put(asset.getSymbol(), new Holding(units, asset.getPrice()));
            } else {
                holding.addUnits(units, asset.getPrice());
            }
            cash -= amount;
            transactions.add(new Transaction("BUY", asset, units, asset.getPrice(), amount, 0));
        }

        public void sell(Asset asset, int units) {
            Holding holding = holdings.get(asset.getSymbol());
            if (holding == null || units <= 0 || units > holding.getUnits()) {
                throw new IllegalArgumentException("Not enough units to sell.");
            }
            double price = asset.getPrice();
            double amount = price * units;
            double profitLoss = (price - holding.getAverageBuyPrice()) * units;
            holding.removeUnits(units);
            if (holding.getUnits() == 0) holdings.remove(asset.getSymbol());
            cash += amount;
            realizedProfitLoss += profitLoss;
            transactions.add(new Transaction("SELL", asset, units, price, amount, profitLoss));
        }

        public double getInvestedCost() {
            double total = 0;
            for (Holding holding : holdings.values()) {
                total += holding.getAverageBuyPrice() * holding.getUnits();
            }
            return total;
        }

        public double getInvestmentValue(List<Asset> assets) {
            double total = 0;
            for (Map.Entry<String, Holding> entry : holdings.entrySet()) {
                Asset asset = findAssetInList(assets, entry.getKey());
                if (asset != null) total += asset.getPrice() * entry.getValue().getUnits();
            }
            return total;
        }

        public double getUnrealizedProfitLoss(List<Asset> assets) {
            return getInvestmentValue(assets) - getInvestedCost();
        }

        public double getTotalValue(List<Asset> assets) {
            return cash + getInvestmentValue(assets);
        }

        public double getCombinedProfitLoss(List<Asset> assets) {
            return realizedProfitLoss + getUnrealizedProfitLoss(assets);
        }

        public int getTradeCount() {
            int count = 0;
            for (Transaction transaction : transactions) {
                if ("BUY".equals(transaction.getAction()) || "SELL".equals(transaction.getAction())) count++;
            }
            return count;
        }

        public void recordMarketUpdate() {
            transactions.add(new Transaction("MARKET", null, 0, 0, 0, 0));
        }

        public void reset(double startingCash) {
            cash = startingCash;
            realizedProfitLoss = 0;
            holdings.clear();
            transactions.clear();
        }

        private Asset findAssetInList(List<Asset> assets, String symbol) {
            for (Asset asset : assets) {
                if (asset.getSymbol().equals(symbol)) return asset;
            }
            return null;
        }
    }

    private static class Transaction {
        private final String action;
        private final String symbol;
        private final String name;
        private final int units;
        private final double unitPrice;
        private final double amount;
        private final double profitLoss;
        private final LocalDateTime timestamp;

        public Transaction(String action, Asset asset, int units, double unitPrice,
                           double amount, double profitLoss) {
            this.action = action;
            this.symbol = asset == null ? "-" : asset.getSymbol();
            this.name = asset == null ? "Market prices updated" : asset.getName();
            this.units = units;
            this.unitPrice = unitPrice;
            this.amount = amount;
            this.profitLoss = profitLoss;
            this.timestamp = LocalDateTime.now();
        }

        public String getAction() { return action; }

        @Override
        public String toString() {
            String time = timestamp.format(DATE_FORMAT);
            if ("MARKET".equals(action)) {
                return time + " | MARKET UPDATE | " + name;
            }
            return String.format(Locale.US,
                    "%s | %-4s | %-9s | units: %d | price: ₹%,.2f | total: ₹%,.2f | P/L: %s",
                    time, action, symbol, units, unitPrice, amount,
                    action.equals("SELL") ? (profitLoss >= 0 ? "+" : "-")
                            + String.format(Locale.US, "₹%,.2f", Math.abs(profitLoss)) : "—");
        }
    }
}