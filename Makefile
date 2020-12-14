.PHONY: build
build:
	dotnet build src --configuration Release

.PHONY: publish
publish:
	dotnet publish src -r win10-x64 -c Release -p:PublishSingleFile=true -p:PublishTrimmed=true


.PHONY: clean
clean:
	dotnet clean src

.PHONY: run
run:
	cd test && dotnet run --project ../src 1 1

.PHONY: acoarse
acoarse:
	cd test/Askervein_coarse && dotnet run --project ../../src 1 7

.PHONY: afine
afine:
	cd test/Askervein_fine && dotnet run --project ../../src 1 7