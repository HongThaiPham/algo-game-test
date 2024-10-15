from algopy import (
    ARC4Contract,
    BoxMap,
    String,
    Txn,
    UInt64,
    arc4,
    op,
)



class MoveStruct(arc4.Struct):
    author: arc4.Address
    color: arc4.String


class MotingApp(ARC4Contract):
    def __init__(self) -> None:
        self.ocuppied_cells = UInt64(0)
        self.move = BoxMap(arc4.UInt64, MoveStruct, key_prefix="")

    @arc4.abimethod
    def make_move(self, move: arc4.UInt64, color: arc4.String) -> None:
      
        assert move < 26 * 26, "Invalid move"
        assert self.ocuppied_cells + 1 < 26 * 26, "Board is full"

        box_data, exists = op.Box.get(move.bytes)
        assert not exists
        # create a box with the move data
        op.Box.put(move.bytes, MoveStruct(author=arc4.Address(Txn.sender), color=color).bytes)
        self.ocuppied_cells += 1

    @arc4.abimethod()
    def hello(self, name: String) -> String:
        return "Hello, " + name
