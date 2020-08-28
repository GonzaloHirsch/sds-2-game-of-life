import java.util.List;

public interface GameOfLife {
    List<int[]> simulateStep();
    double getLivingPercentage();
    double getMaxDistance();
    double calculateMaxDistance();
}
