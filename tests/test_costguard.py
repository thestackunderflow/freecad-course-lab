"""The live cost guard against fc12's two logged runs (Claude Code 2.1.308, claude-sonnet-5-5).

Token totals are the deduplicated usage of out/scratch/fc12/{A1,B1}-session.jsonl at the moment the guard fired;
Claude Code's own /cost for the same runs was $0.1094 / $0.1152. The old raw estimate read ~1.8x high and killed
both runs at a $0.20 cap; the calibrated one must stay at or above /cost (it is a brake) but not kill them."""
import unittest

from lab import costguard as g

A1 = {'input_tokens': 14, 'cache_creation_input_tokens': 33731, 'cache_read_input_tokens': 121865, 'output_tokens': 1687,
      'model': 'claude-sonnet-5-5'}
B1 = {'input_tokens': 14, 'cache_creation_input_tokens': 32648, 'cache_read_input_tokens': 121061, 'output_tokens': 2123,
      'model': 'claude-sonnet-5-5'}
COST = {'A1': 0.1094, 'B1': 0.1152}   # Claude Code's own /cost (pane-cost.txt)


class CostGuard(unittest.TestCase):
    def test_old_raw_estimate_would_kill_at_020(self):
        for tot in (A1, B1):
            self.assertGreater(g.estimate(tot, calib=1.0), 0.20)
            self.assertTrue(g.should_stop(tot, 0.20, calib=1.0))

    def test_calibrated_estimate_does_not_kill(self):
        for tot in (A1, B1):
            self.assertFalse(g.should_stop(tot, 0.20))
            self.assertFalse(g.should_stop(tot, 0.25))

    def test_calibrated_estimate_still_errs_high(self):
        for name, tot in (('A1', A1), ('B1', B1)):
            est = g.estimate(tot)
            self.assertGreaterEqual(est, COST[name])
            self.assertLess(est, COST[name] * 1.25)

    def test_calibrated_still_stops_a_run_past_the_cap(self):
        big = {k: (v * 3 if k != 'model' else v) for k, v in A1.items()}   # ~ $0.33 real
        self.assertTrue(g.should_stop(big, 0.25))


    def test_other_models_keep_the_raw_estimate(self):
        old = dict(A1, model='claude-sonnet-4-6')
        self.assertEqual(g.estimate(old), g.estimate(A1, calib=1.0))

    def test_usage_reads_the_model(self):
        ln = '{"type": "assistant", "message": {"id": "m1", "model": "claude-sonnet-5-5", "usage": {"output_tokens": 10}}}'
        self.assertEqual(g.usage([ln, ln])['model'], 'claude-sonnet-5-5')
        self.assertEqual(g.usage([ln, ln])['output_tokens'], 10)


if __name__ == '__main__':
    unittest.main()
