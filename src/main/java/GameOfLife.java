import java.util.List;

public interface GameOfLife {
    List<int[]> simulateStep();
    int getLivingCellsCount();
    double getMaxDistance();
    double calculateMaxDistance();
}
