# This should be ideally an account that will respond with as many filled fields as possible
SAMPLE_ACCOUNT_ID:=14510744
JTD_INFER:=../../../jtd-infer.exe
JTD_CODEGEN:=../../../jtd-codegen.exe

schemas:= account event

# all: $(patsubst %,%/__init__.py,$(schemas))
.PRECIOUS: $(patsubst %,%-schema-jtd.json,$(schemas))
all: __init__.py


account-sample.json:
	 curl "https://api.new.livestream.com/accounts/${SAMPLE_ACCOUNT_ID}" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0" -H "Accept: */*" -H "Accept-Language: en-US,en;q=0.5" -H "Accept-Encoding: gzip, deflate, br" -H "Pragma: no-cache" -H "Cache-Control: no-cache" > $@

event-sample.json:
	curl "https://api.new.livestream.com/accounts/7451034/events/9468013/videos/228180622" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0" -H "Accept: */*" -H "Accept-Language: en-US,en;q=0.5" -H "Accept-Encoding: gzip, deflate, br" -H "Pragma: no-cache" -H "Cache-Control: no-cache" > $@

%-schema-jtd.json: %-sample.json
	${JTD_INFER} $? > $@

%/__init__.py: %-schema-jtd.json
	mkdir -p $(@:/__init__.py=)
	${JTD_CODEGEN} --python-out $(@:/__init__.py=) $?

__init__.py: livestream-schema-jtd.json
	${JTD_CODEGEN} --python-out . $?
