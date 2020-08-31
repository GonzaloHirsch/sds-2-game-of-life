public enum RuleSet{
    DEFAULT_RULE(1), RULE_2(2), RULE_3(3);

    private int ruleId;

    public int getRuleId(){
        return this.ruleId;
    }

    RuleSet(int id){
        this.ruleId = id;
    }

    static RuleSet fromId(int id){
        switch (id){
            case 1:
                return DEFAULT_RULE;
            case 2:
                return RULE_2;
            case 3:
                return RULE_3;
        }
        return null;
    }

    static int maxRule() {
        return 3;
    }

    static int minRule() {
        return 1;
    }

    @Override
    public String toString() {
        return String.valueOf(ruleId);
    }
}