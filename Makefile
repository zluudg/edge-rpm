.PHONY: package
package:
	docker run \
		--volume ./out:/out \
		tapirbuilder

.PHONY: interact
interact:
	docker run \
		--tty \
		--interactive \
		tapirbuilder \
		bash

.PHONY: builder
builder:
	docker build -t tapirbuilder .
