import java.io.File;
import java.io.FileNotFoundException;
import java.util.Arrays;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        try {
            String filename = args[0];
            int startPoint = Integer.parseInt(args[1]);
            double[][] costs = readFromFile(filename);
            SLS(costs, startPoint);
        }catch(Exception e){
            System.out.println(e.getMessage());
        }
    }

    static int[] bestPath;
    static double minCost;
    static double threshold = 1.8; // Maximum cost ratio we look into
    static long startTime;
    static long timeLimit = (long) 100000000 * 60 * 8; // 8 min

    public static void SLS(double[][] costs, int start){
        int length = costs.length;
        /*
            Init the path by traverse all nodes from start
         */
        bestPath = new int[length];
        for(int i=0; i<length; i++)
            bestPath[i] = (start + i) % length;

        minCost = pathCost(costs, bestPath);

        startTime = System.nanoTime();
        SLSHelper(costs, bestPath, minCost);
        System.out.println("The best path is: " + Arrays.toString(bestPath));
        System.out.println("The cost is: " + minCost);
    }

    private static void SLSHelper(double[][] costs, int[] path, double cost){
        System.out.println(Arrays.toString(path));
        int length = costs.length;

        for(int i=0; i<length - 1; i++){
            /* Stop when reach time limit */
            if(System.nanoTime() - startTime > timeLimit) return;

            /* Try to swap i and i+1 in path */
            double newCost = cost +
                    (i == 0 ? 0 : (costs[path[i-1]][path[i+1]] - costs[path[i-1]][path[i]]))
                    + ((i == length - 2) ? 0 : (costs[path[i]][path[i+2]] - costs[path[i+1]][path[i+2]]));
            /* Keep the change if it's locally better && globally better than the threshold */
            if(newCost < cost && newCost < minCost * threshold){
                int[] newPath = Arrays.copyOf(path, path.length);
                int temp = newPath[i];
                newPath[i] = newPath[i + 1];
                newPath[i + 1] = temp;
                if(newCost < minCost){
                    bestPath = newPath;
                    minCost = newCost;
                }
                SLSHelper(costs, newPath, newCost);
            }
        }
    }

    /* Helper function to get path cost */
    private static int pathCost(double[][] costs, int[] path){
        int total = 0;
        for(int i=1; i<path.length; i++){
            total += costs[path[i-1]][path[i]];
        }
        total += costs[path[path.length - 1]][path[0]];
        return total;
    }

    public static double[][] readFromFile(String filename) throws FileNotFoundException {
        File file = new File(filename);
        Scanner sc = new Scanner(file);
        int length = Integer.parseInt(sc.nextLine());
        double[][] matrix = new double[length][length];
        for(int i=0; i<length; i++){
            String row = sc.nextLine();
            System.out.println(row);
            String[] nums = row.split(" ");
            for(int j=0; j<length; j++){
                matrix[i][j] = Double.parseDouble(nums[j]);
            }
        }
        return matrix;
    }
}