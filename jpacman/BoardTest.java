package nl.tudelft.jpacman.board;

import nl.tudelft.jpacman.board.Square;
import nl.tudelft.jpacman.board.Unit;
import nl.tudelft.jpacman.sprite.PacManSprites;
import nl.tudelft.jpacman.sprite.Sprite;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

public class BoardTest {
    private BasicSquare TestSquare = new BasicSquare();
    private BasicUnit TestUnit = new BasicUnit();

    @Test
    void testPut(){
        //puts Unit on Square
        //then checks to see if Square occupants includes new unit
        TestSquare.put(TestUnit);
        assert TestSquare.getOccupants().contains(TestUnit);
    }

    @Test
    void testRemove(){
        //removes Unit from Square
        //then checks to see if Square occupants does not include unit
        TestSquare.remove(TestUnit);
        assert !TestSquare.getOccupants().contains(TestUnit);
    }

    @Test
    void testHasSquare(){
        //moves Unit to Square
        //then checks to see if hasSquare() is true
        TestUnit.occupy(TestSquare);
        assertThat(TestUnit.hasSquare()).isEqualTo(true);
    }
}
