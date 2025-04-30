> [!warning] I could not get Atheris installed
> On Mac I needed to build LLVM and then Atheris with mismatching toolchains...
> in an Ubuntu container it did not work neither. 
> So no examples

## Idea for a quick example

- [ ] write a function to sort a list
- [ ] write a function to sort a pd.Dataframe
- [ ] write some manual tests
- [ ] write fuzz tests for the list sorting
- [ ] write property based tests for the dataframe?
- [ ] write fuzz & property based tests for the dataframe?


## References

- https://python.plainenglish.io/friendly-fuzzing-tests-in-python-intro-72201778b1b5
- https://google.github.io/oss-fuzz/reference/useful-links/#tutorials
- https://github.com/google/atheris
- https://hypothesis.readthedocs.io/en/latest/reference/api.html#use-with-external-fuzzers
- https://hypothesis.works/articles/intro/
- https://fsharpforfunandprofit.com/posts/property-based-testing-3/