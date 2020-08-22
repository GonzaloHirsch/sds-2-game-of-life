import java.util.List;

public class GameOfLife3D implements GameOfLife{
    private int[][][] board;

    public GameOfLife3D(List<int[][]> layers){
        this.board = new int[layers.size()][layers.get(0).length][layers.get(0)[0].length];

        for (int i = 0; i < layers.size(); i++){
            this.board[i] = layers.get(i);
        }
    }

    public List<int[]> simulateStep() {
        return null;
    }
}
