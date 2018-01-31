#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <inttypes.h>
#include "amqp.h"

///////////////////////////////////////////
// In the test file
#include <gtest/gtest.h>

///////////////////////////////////////////
// Code taken from rabbitmq-c/tests/test_parse_url.c

static int parse_url(const char *url, const char *user,
                          const char *password, const char *host, int port,
                          const char *vhost) {
  char *s = strdup(url);
  struct amqp_connection_info ci;
  memset(&ci, 0, sizeof(amqp_connection_info));
  int res;
 
  amqp_default_connection_info(&ci);  // TODO: Remove me when updating past 0.6.0
  res = amqp_parse_url(s, &ci);
  if (res) {
    fprintf(stderr, "Expected to successfully parse URL, but didn't: %s (%s)\n",
            url, amqp_error_string2(res));
    abort();
  }

  EXPECT_STREQ(user, ci.user);
  EXPECT_STREQ(password, ci.password);
  EXPECT_STREQ(host, ci.host);
  EXPECT_EQ(port, ci.port);
  EXPECT_STREQ(vhost, ci.vhost);

  free(s);
  return res;
}
///////////////////////////////////////////

TEST(rabbitmqTest, Static) {
/* From the spec */
  parse_url("amqp://user:pass@host:10000/vhost", "user", "pass", "host",
                10000, "vhost");
  parse_url("amqps://user:pass@host:10000/vhost", "user", "pass", "host",
                10000, "vhost");

  parse_url("amqp://user%61:%61pass@ho%61st:10000/v%2fhost", "usera",
                "apass", "hoast", 10000, "v/host");
  parse_url("amqps://user%61:%61pass@ho%61st:10000/v%2fhost", "usera",
                "apass", "hoast", 10000, "v/host");

  parse_url("amqp://", "guest", "guest", "localhost", 5672, "/");
  parse_url("amqps://", "guest", "guest", "localhost", 5671, "/");

  parse_url("amqp://:@/", "", "", "localhost", 5672, "");
  parse_url("amqps://:@/", "", "", "localhost", 5671, "");

  parse_url("amqp://user@", "user", "guest", "localhost", 5672, "/");
  parse_url("amqps://user@", "user", "guest", "localhost", 5671, "/");

  parse_url("amqp://user:pass@", "user", "pass", "localhost", 5672, "/");
  parse_url("amqps://user:pass@", "user", "pass", "localhost", 5671, "/");

  parse_url("amqp://host", "guest", "guest", "host", 5672, "/");
  parse_url("amqps://host", "guest", "guest", "host", 5671, "/");

  parse_url("amqp://:10000", "guest", "guest", "localhost", 10000, "/");
  parse_url("amqps://:10000", "guest", "guest", "localhost", 10000, "/");

  parse_url("amqp:///vhost", "guest", "guest", "localhost", 5672, "vhost");
  parse_url("amqps:///vhost", "guest", "guest", "localhost", 5671, "vhost");

  parse_url("amqp://host/", "guest", "guest", "host", 5672, "");
  parse_url("amqps://host/", "guest", "guest", "host", 5671, "");

  parse_url("amqp://host/%2f", "guest", "guest", "host", 5672, "/");
  parse_url("amqps://host/%2f", "guest", "guest", "host", 5671, "/");

  parse_url("amqp://[::1]", "guest", "guest", "::1", 5672, "/");
  parse_url("amqps://[::1]", "guest", "guest", "::1", 5671, "/");

  /* Various other success cases */
  parse_url("amqp://host:100", "guest", "guest", "host", 100, "/");
  parse_url("amqps://host:100", "guest", "guest", "host", 100, "/");

  parse_url("amqp://[::1]:100", "guest", "guest", "::1", 100, "/");
  parse_url("amqps://[::1]:100", "guest", "guest", "::1", 100, "/");

  parse_url("amqp://host/blah", "guest", "guest", "host", 5672, "blah");
  parse_url("amqps://host/blah", "guest", "guest", "host", 5671, "blah");

  parse_url("amqp://host:100/blah", "guest", "guest", "host", 100, "blah");
  parse_url("amqps://host:100/blah", "guest", "guest", "host", 100, "blah");

  parse_url("amqp://:100/blah", "guest", "guest", "localhost", 100, "blah");
  parse_url("amqps://:100/blah", "guest", "guest", "localhost", 100,
                "blah");

  parse_url("amqp://[::1]/blah", "guest", "guest", "::1", 5672, "blah");
  parse_url("amqps://[::1]/blah", "guest", "guest", "::1", 5671, "blah");

  parse_url("amqp://[::1]:100/blah", "guest", "guest", "::1", 100, "blah");
  parse_url("amqps://[::1]:100/blah", "guest", "guest", "::1", 100, "blah");

  parse_url("amqp://user:pass@host", "user", "pass", "host", 5672, "/");
  parse_url("amqps://user:pass@host", "user", "pass", "host", 5671, "/");

  parse_url("amqp://user:pass@host:100", "user", "pass", "host", 100, "/");
  parse_url("amqps://user:pass@host:100", "user", "pass", "host", 100, "/");

  parse_url("amqp://user:pass@:100", "user", "pass", "localhost", 100, "/");
  parse_url("amqps://user:pass@:100", "user", "pass", "localhost", 100,
                "/");

  parse_url("amqp://user:pass@[::1]", "user", "pass", "::1", 5672, "/");
  parse_url("amqps://user:pass@[::1]", "user", "pass", "::1", 5671, "/");

  parse_url("amqp://user:pass@[::1]:100", "user", "pass", "::1", 100, "/");
  parse_url("amqps://user:pass@[::1]:100", "user", "pass", "::1", 100, "/");
}
