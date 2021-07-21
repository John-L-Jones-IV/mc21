class StrategyTable():
    #TODO: soft, surrender, and split tables

    def str_to_enum(c):
        if (c == 'H'):
            return Call.HIT
        elif (c == 'D'):
            return Call.DOUBLE
        elif (c == 'S'):
            return Call.SPLIT
        elif (c == 'Su'):
            return Call.SURRENDER
        elif (c == 'I'):
            return Call.SURRENDER
        elif (c == 'S'):
            return Call.STAND
        else:
            raise ValueError(c, 'is not a valid input. Check .strat file')

    def __init__(self, path_to_csv) -> None:
        """Build nested dict model from importing from a custom *.strat file."""
        strat = dict(zip(range(2,12),[dict()]*10))

        # open file and poplulate nested dict()
        with open(path_to_csv, 'r') as f:
            read_data = f.read()
        read_data = read_data.replace(' ', '')
        read_data = read_data.replace('\n', '')
        read_data = read_data.split(',')
        READ_DATA_OFFSET = 11
        ROW_STEP = 11
        for row in range(2, 22):
            for col in range(2, 12):
                idx = (row-2)*ROW_STEP + (col-2) + READ_DATA_OFFSET
                strat[col][row] = read_data[idx]

        self.strat = strat


class Strategy(ABC):

    @abstractmethod
    def strategy_call(
            self,
            hand : CardCollection,
            dealer_top_card : int,
            card_counted_deck : CardCollection):
        pass


class SimpleStrategy(Strategy):

    def __init__(self, hit_until_val : int) -> None:
        self.hit_until_val = hit_until_val

    def strategy_call(
            self,
            hand,
            dealer_top_card=None,
            card_counted_deck=None):
        if sum(hand) < self.hit_until_val:
            return Call.HIT
        return Call.STAND


class BasicStrategy(Strategy):

    def __init__(
            self,
            hard_table: StrategyTable,
            soft_table: StrategyTable,
            split_table: StrategyTable,
            surrender_table: StrategyTable):
        self.hard_table = hard_table
        self.soft_table = soft_table
        self.split_table = split_table
        self.surrender_table = surrender_table


class ProbTreeStrategy(Strategy):
    pass


class MLStrategy(Strategy):
    pass


class HLStrategy(Strategy):
    pass
