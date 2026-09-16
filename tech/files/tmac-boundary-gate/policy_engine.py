class PolicyEngine:
    """
    v0.1 threshold policy:
      score < 0.5    -> allow
      0.5~0.8        -> sanitize
      >= 0.8         -> block
    """
    def decide(self, score: float) -> str:
        if score < 0.5:
            return "allow"
        elif score < 0.8:
            return "sanitize"
        else:
            return "block"
