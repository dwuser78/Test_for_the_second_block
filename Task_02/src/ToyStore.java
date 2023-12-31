import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class ToyStore {
    private List<Toy> toys = new ArrayList<>();
    private List<Toy> prizeToys = new ArrayList<>();
    private Random random = new Random();

    public void addToy(Toy toy) {
        toys.add(toy);
    }

    public void editToyProbability(int id, double probability) {
        for (Toy toy : toys) {
            if (toy.getId() == id) {
                toy.setProbability(probability);
                break;
            }
        }
    }

    public List getPrizeToys() {
        return prizeToys;
    }

    public Toy play() {
        double totalProbability = 0;
        for (Toy toy : toys) {
            totalProbability += toy.getProbability();
        }
        double randomProbability = random.nextDouble() * totalProbability;
        double probabilitySum = 0;
        for (Toy toy : toys) {
            probabilitySum += toy.getProbability();
            if (randomProbability <= probabilitySum) {
                prizeToys.add(toy);
                toy.setQuantity(toy.getQuantity() - 1);
                return toy;
            }
        }
        return null;
    }
}