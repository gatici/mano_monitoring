pushd simple
        charmcraft  build
        cp -r  build/prime/*  .
        cp -r  venv/ops  src/
popd

