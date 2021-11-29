# TennisSim
Tennis game simulator written in Python (version 3.9).
This simulator uses two threads who rely on events as two players.
Rules of the game - 
- Every player gets to serve twice a row
- Whoever wins the last point in a serve, gets to have the next serve.
- Without a 10-10 tie whoever gets 11th point wins the set.
- At 10-10 tie, every player strives for a two point lead until one of them achieves it or reaches the score 21.

# Running the code - 
`python tennis_sim_thread.py`
This will log the serving player, live scoring and match end with winner and their score.

# Running tests - 
Using `pytest`, tests are integrated within the file, since the code is small.
The `pytest.ini` file makes sure that all `INFO` logs are printed while running the tests.

To run all tests - `pytest tennis_sim_thread.py --html=report.html` - will generate test report in directory.

To run a single test - `pytest tennis_sim_thread.py::test_set --html=report.html`
