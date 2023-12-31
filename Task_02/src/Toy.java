public class Toy {
    private int id;
    private String name;
    private int quantity;
    private double probability;

    public Toy(int id, String name, int quantity, double probability) {
        this.id = id;
        this.name = name;
        this.quantity = quantity;
        this.probability = probability;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getQuantity() {
        return quantity;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }

    public double getProbability() {
        return probability;
    }

    public void setProbability(double probability) {
        this.probability = probability;
    }
}
