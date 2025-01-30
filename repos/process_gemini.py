import vertexai
from vertexai.preview.generative_models import GenerativeModel, GenerationConfig
import os
import time

#with open("queries.txt") as f:

print(os.getcwd())


#    sample_queries = f.read()


pr_question = """
Closes #3143

Will throw a RangeError if status code:
is less than 100
is greater than 999
This aligns with Node.js' behavior of throwing if given something outside that range

Will throw a TypeError if status code is:
Not an integer (string representation of integer included)
This is a choice we are making to limit the acceptable input.

Use res.status internally when setting status codes
the PR also ensures we use res.status internally when setting status codes, to allow us to use the validation logic internally.

Test changes
I cleaned up the tests to test acceptable range, and invalid codes, and removed the iojs logic as its not supported in v5.

TODO:
 Update the PR description to be specific to the actual changes in this PR, possibly reopen the PR since direction has changed
Notably, this PR currently throws on strings, redefines the valid range of codes to between 1xx and 9xx, throws on non-integer floats (e.g. 500.5, but allows 500.00 bc it is the same to JS), throws a RangeError if we get a status code outside 1xx to 9xx range
 Ensure the tests are accurate to these changes, and clean up the tests in here
 Update the v5 docs to reflect said changes (separate PR to expressjs.com)
related: expressjs/discussions#233

dougwilson suggested changes on Mar 10, 2020
test/res.status.js
Outdated
@dougwilson dougwilson added the pr label on Mar 10, 2020
@jonchurch
Member
Author
jonchurch commented on Mar 10, 2020
I realized after opening this that Node.js does not throw on inputs like 500.5, this PR however does. From the other PR, I think we decided to throw on these cases, but I wanted to make clear that from my limited testing Node.js is not throwing on floats.

@gireeshpunathil
Contributor
gireeshpunathil commented on Mar 10, 2020
I wanted to make clear that from my limited testing Node.js is not throwing on floats.

@jonchurch - my assertion is that 500.5 is definitely invalid, so throwing is the right thing to do.

@dougwilson
Contributor
dougwilson commented on Mar 10, 2020
Yea, I don't have any issues with this throwing on a float; we want to throw on whatever Node.js throws on as the minimum bar. If we can also help the users by also throwing on definitely nonsensical inputs (like status codes with fractions) that makes sense of course :) !

@jonchurch
This comment was marked as outdated.
Show comment
LinusU
LinusU reviewed on Mar 10, 2020
lib/response.js
Outdated
@dougwilson
This comment was marked as outdated.
Show comment
@gireeshpunathil gireeshpunathil mentioned this pull request on Mar 13, 2020
Express TC Meeting 03-18-2020 expressjs/discussions#109
Closed
@gireeshpunathil
Contributor
gireeshpunathil commented on Mar 20, 2020
as per the TC discussion, this is ready to merge, who is going to do that? @dougwilson , I see your red-X on this - is that still valid, or you are going to remove it and land?

@jonchurch jonchurch mentioned this pull request on Mar 21, 2020
Deprecate non integer status codes in v4 #4223
 Merged
@dougwilson dougwilson added 5.x enhancement labels on Mar 25, 2020
@jonchurch jonchurch added this to the 5.0 milestone on Apr 1, 2020
@jonchurch
Member
Author
jonchurch commented on Apr 1, 2020 • 
Thinking more about this and something bothers me. I took the approach the previous PR did, since it had been reviewed, but now I'm questioning the use of res.status internally to set statuses.

If someone monkey-patches res.status it will alter the internal behavior of setting status codes on responses. That's not different though for other functions used in response, like res.type for example.

My question has two parts:

Is it a breaking change to be relying on res.status() to set status codes internally?
Do we want to distinguish between private vs public methods? (there are only two things marked private in response according to jsdoc comments)
See an example of the change in the diff: https://github.com/expressjs/express/pull/4212/files#diff-d86a59ede7d999db4b7bc43cb25a1c11L137-R142

@dougwilson
Contributor
dougwilson commented on Apr 1, 2020
Is it a breaking change to be relying on res.status() to set status codes internally?

Yes, as stated in #4223 (comment) , but this PR is already a breaking change, right? So I'm not sure if it's super relevant. The change itself makes sense to make, just like we call res.type internally and not directly get the content-type response header. Even getting headers we internally use req.get and not req.headers.

Do we want to distinguish between private vs public methods? (there are only two things marked private in response according to jsdoc comments)

I'm not really following on what this part of the question really is. The main reason the internals use Express' own API is especially useful for AOP type of design patterns, if the user so chooses to do them. The Node.js HTTP APIs do the same patterns as well, AFAIK.

@jonchurch
Member
Author
jonchurch commented on Apr 1, 2020
I wasn't clear. Re: breaking, I meant that someone's v4 res.status monkey patch might affect code in unexpected ways under v5, because it is used in more places than before.

You've answered my second question I believe. We aren't interested in making some methods private and off limits to users.

Thanks, I wanted to bring up this point (re: effects of monkey-patching res.status with these changes) just so someone else could check it.

Realizing that we use a lot of these helper methods internally would indicate that this change is not out of step with what is standard.

@jonchurch
Member
Author
jonchurch commented on Apr 1, 2020
Just read that linked comment and saw you did directly address the concern already 👍

@dougwilson
Contributor
dougwilson commented on Apr 2, 2020
Yep! I did, though, not directly address the monkey patching messing something up; that is indeed the case, but I don't think any more so than other aspects of Node.js and Javascript. I think that it is going to be possible for users to override something and cause a breakage, but I'm not sure that the effort in order to prevent such a thing is really worth it. From support experience, I think it is extremely rare for such an issue to really show up, haha.

@jonchurch jonchurch mentioned this pull request on Apr 19, 2020
Gracefully handle invalid status codes #3143
 Closed
@dougwilson dougwilson mentioned this pull request on May 23, 2021
Check for invalid or unknown http status codes. #4598
 Closed
@dougwilson dougwilson force-pushed the master branch from c0e5dc1 to 6660649 
4 years ago
@dougwilson dougwilson force-pushed the master branch from 2295290 to a84e73b 
3 years ago
@dougwilson dougwilson force-pushed the master branch from 04f6451 to 4ed35b4 
3 years ago
@dougwilson dougwilson force-pushed the master branch 2 times, most recently from eb10dba to 340be0f 
3 years ago
@abenhamdine
Contributor
abenhamdine commented on Mar 10, 2023
I think this PR should target branch https://github.com/expressjs/express/tree/5.0 and not master.
And if it's ok, it should be merged aswell in v5 branch.

@wesleytodd wesleytodd mentioned this pull request on Mar 21, 2024
Release 5.0 #2237
 Merged
39 tasks
@UlisesGascon UlisesGascon mentioned this pull request on Apr 25, 2024
Express 5.0 - last push! expressjs/discussions#233
Closed
46 tasks
35 hidden items
Load more…
@jonchurch jonchurch marked this pull request as ready for review 9 months ago
blakeembrey
blakeembrey reviewed on May 4, 2024
lib/response.js
Outdated
lib/response.js
Outdated
lib/response.js
@jonchurch jonchurch requested a review from a team 8 months ago
wesleytodd
wesleytodd reviewed on May 15, 2024
Member
wesleytodd left a comment
Some of the comments are unaddressed, so didn't want to approve, but I think once those are addressed this looks good.

lib/response.js
jonchurch added 2 commits 7 months ago
@jonchurch
stringify code in thrown RangeError message
64e8576
@jonchurch
remove accidentally duplicated res.status method
4dbf773
@jonchurch jonchurch requested review from blakeembrey and wesleytodd 7 months ago
ctcpip
ctcpip previously requested changes on Jun 6, 2024
History.md
Outdated
lib/response.js
@jonchurch
@ctcpip
fix error range message 
bf4541b
jonchurch
jonchurch commented on Jun 8, 2024
test/res.sendStatus.js
Outdated
@jonchurch
update sendStatus invalid code test to use sendStatus
794f2de
@jonchurch jonchurch requested a review from ctcpip 6 months ago
@jonchurch jonchurch dismissed ctcpip’s stale review 6 months ago
addressed

wesleytodd
wesleytodd approved these changes on Jul 27, 2024
@jonchurch jonchurch changed the base branch from 5.x to 5.0 6 months ago
blakeembrey
blakeembrey approved these changes on Jul 27, 2024
@wesleytodd
Member
wesleytodd commented on Jul 30, 2024
I am landing this despite the pending 22 test and the coverage report. I think we agree it is good and if we have to fix CI we can do it along with dropping node 18. I am getting to the point where I think we should merge all these pending ones and live with 5.0 being broken until we land the node@18 change anyway.

@wesleytodd wesleytodd merged commit 723b545 into expressjs:5.0 on Jul 30, 2024
19 of 20 checks passed
This was referenced on Oct 28, 2024
[Snyk] Upgrade express from 4.21.1 to 5.0.0 nerdy-tech-com-gitub/images#2
 Open
[Snyk] Upgrade express from 4.21.1 to 5.0.0 nerdy-tech-com-gitub/chroma#15
 Open
[Snyk] Upgrade express from 4.21.1 to 5.0.0 nerdy-tech-com-gitub/images#8
 Open
@EchoSkorJjj EchoSkorJjj mentioned this pull request on Oct 29, 2024
[Snyk] Upgrade express from 4.18.2 to 5.0.0 EchoSkorJjj/UI#277
 Open
This was referenced on Oct 30, 2024
[Snyk] Upgrade express from 4.21.1 to 5.0.0 SherfeyInv/images#3
 Open
[Snyk] Upgrade express from 4.21.1 to 5.0.0 SherfeyInv/images#4
 Open
@Gabo-Tech Gabo-Tech mentioned this pull request on Nov 3, 2024
[Snyk] Upgrade express from 4.16.3 to 5.0.0 Gabo-Tech/toDoList#316
 Open
@EchoSkorJjj EchoSkorJjj mentioned this pull request on Nov 6, 2024
[Snyk] Upgrade express from 4.18.2 to 5.0.0 EchoSkorJjj/UI#278
 Open
@snyk-io snyk-io bot mentioned this pull request on Nov 10, 2024
[Snyk] Upgrade express from 4.21.1 to 5.0.0 doperiddle/bch-rpc-explorer#11
 Open
@doperiddle doperiddle mentioned this pull request on Nov 10, 2024
[Snyk] Upgrade express from 4.17.1 to 5.0.0 doperiddle/paystring#5
 Merged
@Gabo-Tech Gabo-Tech mentioned this pull request on Nov 10, 2024
[Snyk] Upgrade express from 4.16.3 to 5.0.0 Gabo-Tech/toDoList#318
"""

pr_diff = """diff --git a/History.md b/History.md
index 73fc46b26f..89d5af3ceb 100644
--- a/History.md
+++ b/History.md
@@ -1,3 +1,10 @@
+unreleased
+=========================
+* breaking:
+  * `res.status()` accepts only integers, and input must be greater than 99 and less than 1000
+    * will throw a `RangeError: Invalid status code: ${code}. Status code must be greater than 99 and less than 1000.` for inputs outside this range
+    * will throw a `TypeError: Invalid status code: ${code}. Status code must be an integer.` for non integer inputs
+
 5.0.0-beta.3 / 2024-03-25
 =========================
 
diff --git a/lib/response.js b/lib/response.js
index 14743817a9..6ad54dbfc7 100644
--- a/lib/response.js
+++ b/lib/response.js
@@ -15,7 +15,6 @@
 var Buffer = require('safe-buffer').Buffer
 var contentDisposition = require('content-disposition');
 var createError = require('http-errors')
-var deprecate = require('depd')('express');
 var encodeUrl = require('encodeurl');
 var escapeHtml = require('escape-html');
 var http = require('http');
@@ -57,17 +56,28 @@ module.exports = res
 var schemaAndHostRegExp = /^(?:[a-zA-Z][a-zA-Z0-9+.-]*:)?\/\/[^\\\/\?]+/;
 
 /**
- * Set status `code`.
+ * Set the HTTP status code for the response.
  *
- * @param {Number} code
- * @return {ServerResponse}
+ * Expects an integer value between 100 and 999 inclusive.
+ * Throws an error if the provided status code is not an integer or if it's outside the allowable range.
+ *
+ * @param {number} code - The HTTP status code to set.
+ * @return {ServerResponse} - Returns itself for chaining methods.
+ * @throws {TypeError} If `code` is not an integer.
+ * @throws {RangeError} If `code` is outside the range 100 to 999.
  * @public
  */
 
 res.status = function status(code) {
-  if ((typeof code === 'string' || Math.floor(code) !== code) && code > 99 && code < 1000) {
-    deprecate('res.status(' + JSON.stringify(code) + '): use res.status(' + Math.floor(code) + ') instead')
+  // Check if the status code is not an integer
+  if (!Number.isInteger(code)) {
+    throw new TypeError(`Invalid status code: ${JSON.stringify(code)}. Status code must be an integer.`);
   }
+  // Check if the status code is outside of Node's valid range
+  if (code < 100 || code > 999) {
+    throw new RangeError(`Invalid status code: ${JSON.stringify(code)}. Status code must be greater than 99 and less than 1000.`);
+  }
+
   this.statusCode = code;
   return this;
 };
@@ -182,7 +192,7 @@ res.send = function send(body) {
   }
 
   // freshness
-  if (req.fresh) this.statusCode = 304;
+  if (req.fresh) this.status(304);
 
   // strip irrelevant headers
   if (204 === this.statusCode || 304 === this.statusCode) {
@@ -314,7 +324,7 @@ res.jsonp = function jsonp(obj) {
 res.sendStatus = function sendStatus(statusCode) {
   var body = statuses.message[statusCode] || String(statusCode)
 
-  this.statusCode = statusCode;
+  this.status(statusCode);
   this.type('txt');
 
   return this.send(body);
@@ -847,7 +857,7 @@ res.redirect = function redirect(url) {
   });
 
   // Respond
-  this.statusCode = status;
+  this.status(status);
   this.set('Content-Length', Buffer.byteLength(body));
 
   if (this.req.method === 'HEAD') {
diff --git a/test/res.sendStatus.js b/test/res.sendStatus.js
index 9b1de8385c..b244cf9d17 100644
--- a/test/res.sendStatus.js
+++ b/test/res.sendStatus.js
@@ -28,5 +28,17 @@ describe('res', function () {
       .get('/')
       .expect(599, '599', done);
     })
+
+    it('should raise error for invalid status code', function (done) {
+      var app = express()
+
+      app.use(function (req, res) {
+        res.sendStatus(undefined).end()
+      })
+
+      request(app)
+        .get('/')
+        .expect(500, /TypeError: Invalid status code/, done)
+    })
   })
 })
diff --git a/test/res.status.js b/test/res.status.js
index d2fc6a28c1..59c8a57e70 100644
--- a/test/res.status.js
+++ b/test/res.status.js
@@ -1,59 +1,36 @@
 'use strict'
-
-var express = require('../')
-var request = require('supertest')
-
-var isIoJs = process.release
-  ? process.release.name === 'io.js'
-  : ['v1.', 'v2.', 'v3.'].indexOf(process.version.slice(0, 3)) !== -1
+const express = require('../.');
+const request = require('supertest');
 
 describe('res', function () {
   describe('.status(code)', function () {
-    // This test fails in node 4.0.0
-    // https://github.com/expressjs/express/pull/2237/checks
-    // As this will all be removed when https://github.com/expressjs/express/pull/4212
-    // lands I am skipping for now and we can delete with that PR
-    describe.skip('when "code" is undefined', function () {
-      it('should raise error for invalid status code', function (done) {
-        var app = express()
 
-        app.use(function (req, res) {
-          res.status(undefined).end()
-        })
+    it('should set the status code when valid', function (done) {
+      var app = express();
 
-        request(app)
-          .get('/')
-          .expect(500, /Invalid status code/, function (err) {
-            if (isIoJs) {
-              done(err ? null : new Error('expected error'))
-            } else {
-              done(err)
-            }
-          })
-      })
-    })
+      app.use(function (req, res) {
+        res.status(200).end();
+      });
 
-    describe.skip('when "code" is null', function () {
-      it('should raise error for invalid status code', function (done) {
+      request(app)
+        .get('/')
+        .expect(200, done);
+    });
+
+    describe('accept valid ranges', function() {
+      // not testing w/ 100, because that has specific meaning and behavior in Node as Expect: 100-continue
+      it('should set the response status code to 101', function (done) {
         var app = express()
 
         app.use(function (req, res) {
-          res.status(null).end()
+          res.status(101).end()
         })
 
         request(app)
           .get('/')
-          .expect(500, /Invalid status code/, function (err) {
-            if (isIoJs) {
-              done(err ? null : new Error('expected error'))
-            } else {
-              done(err)
-            }
-          })
+          .expect(101, done)
       })
-    })
 
-    describe('when "code" is 201', function () {
       it('should set the response status code to 201', function (done) {
         var app = express()
 
@@ -65,9 +42,7 @@ describe('res', function () {
           .get('/')
           .expect(201, done)
       })
-    })
 
-    describe('when "code" is 302', function () {
       it('should set the response status code to 302', function (done) {
         var app = express()
 
@@ -79,9 +54,7 @@ describe('res', function () {
           .get('/')
           .expect(302, done)
       })
-    })
 
-    describe('when "code" is 403', function () {
       it('should set the response status code to 403', function (done) {
         var app = express()
 
@@ -93,9 +66,7 @@ describe('res', function () {
           .get('/')
           .expect(403, done)
       })
-    })
 
-    describe('when "code" is 501', function () {
       it('should set the response status code to 501', function (done) {
         var app = express()
 
@@ -107,100 +78,129 @@ describe('res', function () {
           .get('/')
           .expect(501, done)
       })
-    })
 
-    describe('when "code" is "410"', function () {
-      it('should set the response status code to 410', function (done) {
+      it('should set the response status code to 700', function (done) {
         var app = express()
 
         app.use(function (req, res) {
-          res.status('410').end()
+          res.status(700).end()
         })
 
         request(app)
           .get('/')
-          .expect(410, done)
+          .expect(700, done)
       })
-    })
 
-    describe.skip('when "code" is 410.1', function () {
-      it('should set the response status code to 410', function (done) {
+      it('should set the response status code to 800', function (done) {
         var app = express()
 
         app.use(function (req, res) {
-          res.status(410.1).end()
+          res.status(800).end()
         })
 
         request(app)
           .get('/')
-          .expect(410, function (err) {
-            if (isIoJs) {
-              done(err ? null : new Error('expected error'))
-            } else {
-              done(err)
-            }
-          })
+          .expect(800, done)
       })
-    })
 
-    describe.skip('when "code" is 1000', function () {
-      it('should raise error for invalid status code', function (done) {
+      it('should set the response status code to 900', function (done) {
         var app = express()
 
         app.use(function (req, res) {
-          res.status(1000).end()
+          res.status(900).end()
         })
 
         request(app)
           .get('/')
-          .expect(500, /Invalid status code/, function (err) {
-            if (isIoJs) {
-              done(err ? null : new Error('expected error'))
-            } else {
-              done(err)
-            }
-          })
+          .expect(900, done)
       })
     })
 
-    describe.skip('when "code" is 99', function () {
-      it('should raise error for invalid status code', function (done) {
-        var app = express()
+    describe('invalid status codes', function () {
+      it('should raise error for status code below 100', function (done) {
+        var app = express();
 
         app.use(function (req, res) {
-          res.status(99).end()
-        })
+          res.status(99).end();
+        });
 
         request(app)
           .get('/')
-          .expect(500, /Invalid status code/, function (err) {
-            if (isIoJs) {
-              done(err ? null : new Error('expected error'))
-            } else {
-              done(err)
-            }
-          })
-      })
-    })
+          .expect(500, /Invalid status code/, done);
+      });
 
-    describe.skip('when "code" is -401', function () {
-      it('should raise error for invalid status code', function (done) {
-        var app = express()
+      it('should raise error for status code above 999', function (done) {
+        var app = express();
 
         app.use(function (req, res) {
-          res.status(-401).end()
-        })
+          res.status(1000).end();
+        });
 
         request(app)
           .get('/')
-          .expect(500, /Invalid status code/, function (err) {
-            if (isIoJs) {
-              done(err ? null : new Error('expected error'))
-            } else {
-              done(err)
-            }
-          })
-      })
-    })
-  })
-})
+          .expect(500, /Invalid status code/, done);
+      });
+
+      it('should raise error for non-integer status codes', function (done) {
+        var app = express();
+
+        app.use(function (req, res) {
+          res.status(200.1).end();
+        });
+
+        request(app)
+          .get('/')
+          .expect(500, /Invalid status code/, done);
+      });
+
+      it('should raise error for undefined status code', function (done) {
+        var app = express();
+
+        app.use(function (req, res) {
+          res.status(undefined).end();
+        });
+
+        request(app)
+          .get('/')
+          .expect(500, /Invalid status code/, done);
+      });
+
+      it('should raise error for null status code', function (done) {
+        var app = express();
+
+        app.use(function (req, res) {
+          res.status(null).end();
+        });
+
+        request(app)
+          .get('/')
+          .expect(500, /Invalid status code/, done);
+      });
+
+      it('should raise error for string status code', function (done) {
+        var app = express();
+
+        app.use(function (req, res) {
+          res.status("200").end();
+        });
+
+        request(app)
+          .get('/')
+          .expect(500, /Invalid status code/, done);
+      });
+
+      it('should raise error for NaN status code', function (done) {
+        var app = express();
+
+        app.use(function (req, res) {
+          res.status(NaN).end();
+        });
+
+        request(app)
+          .get('/')
+          .expect(500, /Invalid status code/, done);
+      });
+    });
+  });
+});
+"""


system_instruction = (
    "You are an expert programmer at a leading FAANG technology company. \n"
    "You have been given a software repository for analysis. \n"
    "The code files are provided in the format: <CODEFILE><file path>...</CODEFILE>, where <file path> is the file path within the repository, and '...' is the file content. \n"
    "You are also given the following github issue discussion: <GITHUB_DISCUSSION>{pr_question}</GITHUB_DISCUSSION>;\n"
    "And you are given github difference introduced by commit: <GITHUB_DIFFERENCE>{pr_diff}</GITHUB_DIFFERENCE>.\n\n"


    "Your task is to understand the key points and logic of the codebase and suggest the additional code files you need to implement the requested change, beyond the ones that were changed by commit. \n"
    
    "Steps to formulate questions: \n"
    "1. Identify key components and their roles within the system. \n"
    "2. Identify the files which were modified in the provided git diff and the logic which was added, removed or changed. \n"
    "3. Examine the diff code snippets and related code for classes, objects, declarations, implementations, components, variables and other enitites which are used in the provided git diff. \n"
    "4. Consider indirect connections or implications in the code related to the topic discussed in the pull request. \n"
    "5. Determine the relevant code files, including dependent files necessary for understanding the enitities and the logic in the provided git diff - any additional declarations, definitions, imports, class bodies, functions, etc from the ther parts of the codebsase. \n"
    "6. Determine all the additional files which are not directly related but are necessary to understand the implementation in relevant code files from step 5). \n "
    "7. Carefully assess for all the selected files if they are required for you to understand and implement the changes requested.\n"
    "8. Score the importance of each additional file on the scale 1-10 depending on how much it is needed to understand the git diff requested.\n"
    #"9. Remove from the list files with low importance 1-2. \n"
    #"9. Prepate list of scored files, then sort the files by score, select and output max top 20 files according to their scores.\n" 

    "Output only those files with scores in JSON format: {{'relative/path/to/file1': score, 'relative/path/to/file2':score, ...}}, do not explain your reasoning or provide any comments.\n"
    "Please do not include the files which were already modified in the provided git diff, your task is to determine the additional files needed to understand the code and diff. \n"
)


vertexai.init(project="thinking-bonbon-408005")#, location="europe-west4")


def query_gemini(files, pr_question, pr_diff, max_retries=8, base_delay=2):
    gemini_model = GenerativeModel('gemini-2.0-flash-exp', system_instruction=system_instruction.format(pr_question=pr_question, pr_diff=pr_diff)) # gemini-flash has 32k context window, for big context use 'gemini-1.5-pro'

    query = ""
    for filename, contents in files.items():
        query += f"<CODEFILE><{filename}>{contents}</CODEFILE>\n"

    query = query[:int(3*1000000)]

    
    for attempt in range(max_retries):
        try:
            
            generation_config = GenerationConfig(
              temperature=0.,
          )

            response = gemini_model.generate_content(f"Repository to analyze:\n{query}", generation_config=generation_config)
            return response.text.strip()
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if "The input token count" in str(e):
                print("Reducing query by 30%")
                query = query[:-int(len(query)*0.3)] # Remove 30% of the last chunk
            if attempt < max_retries - 1:
                delay = base_delay #* (2 ** attempt)  # Exponential backoff
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
    
    print("All attempts failed. Returning an empty string.")
    return ""

def read_py_files_from_repo(repo_path, extensions=None):
    if extensions is None:
        # Default to common code file extensions
        extensions = ['.dart','.gradle', '.yaml', '.m', '.py', '.svelte', '.sh', '.css', '.html', '.java', '.cpp', '.h', '.hpp','.c', '.cs', '.rb', '.go', '.php', '.swift', '.kt', '.rs', '.md', '.ts', '.js', '.jsx']

    code_files = {}
    for root, _, files in os.walk(repo_path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                # Check if the file is a symbolic link and skip it if so
                if os.path.islink(file_path):
                    continue
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    code_files[file_path] = f.read()
    return code_files


if __name__ == "__main__":

    repo_path = 'repos/express'

    py_files = read_py_files_from_repo(repo_path)

    gemini_result = query_gemini(py_files, pr_question, pr_diff)

    print(gemini_result)