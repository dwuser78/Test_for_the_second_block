import java.io.FileWriter;
import java.util.List;

public class Main {
    public static void savePrizeToy(String filename, Toy prizeToy) {
        try {
            FileWriter fileWriter = new FileWriter(filename, true);
            fileWriter.write(prizeToy.getId() + "\n");
            fileWriter.close();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public static void main(String[] args) {
        String filename = "toys.txt";
        ToyStore toyStore = new ToyStore();

        toyStore.addToy(new Toy(1, "Toy 1", 10, 50));
        toyStore.addToy(new Toy(2, "Toy 2", 5, 75));
        toyStore.addToy(new Toy(3, "Toy 3", 3, 90));

        Toy prizeToy = toyStore.play();

        if (prizeToy == null) {
            System.out.println("All prizes have been awarded");
        } else {
            System.out.println("You have won " + prizeToy.getName());

            List prizeToys = toyStore.getPrizeToys();
            prizeToys.add(prizeToy);

            savePrizeToy(filename, prizeToy);
        }
    }
}