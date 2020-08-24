import java.util.List;

public interface GameOfLife {
    List<int[]> simulateStep();
    double getMaxDistance();
    double calculateMaxDistance();
}
