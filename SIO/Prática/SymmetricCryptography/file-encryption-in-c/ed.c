// Author: André Zúquete <andre.zuquete@ua.pt>

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <memory.h>
#include <libgen.h>

#include <openssl/evp.h>
#include <openssl/rand.h>
#include <openssl/aes.h>

#include "key.h"

int
main( int argc, char * argv[] )
{
    EVP_CIPHER_CTX * ctx;
    uint8_t * iv = 0;
    int iv_len = 0;
    uint8_t in[4096];
    uint8_t out[4096];
    int in_len, out_len;
    char * command;
    int encrypt;

    if (argc != 3) {
        fprintf( stderr, "Usage: %s passwd algorithm\n", argv[0] );
        return 1;
    }

    command = basename( argv[0] );


    if (strcmp( command, "enc" ) != 0 && strcmp( command, "dec" ) != 0) {
        fprintf( stderr, "Command \"%s\" must be named \"enc\" or \"dec\"\n", command );
        return 1;
    }

    // encrypt != 0 -> encryption operation
    // encrypt == 0 -> decryption operation

    encrypt = strcmp( command, "dec" );

    ctx = set_ctx( argv[1], argv[2], encrypt, &iv, &iv_len );

    if (ctx == 0 && iv == 0) {
        fprintf( stderr, "Error in context setup, aborting.\n" );
        return 1;
    }

    // Non null IV buffer means that either the IV was generated (and needs to be written) or needs to be red

    if (iv) {
        if (encrypt) {
            fprintf( stderr, "Write IV first ...\n" );
            write( 1, iv, iv_len );
        }
        else {
            fprintf( stderr, "Read IV first ...\n" );
            read( 0, iv, iv_len );

            // Create context after getting first the IV

            ctx = set_ctx( argv[1], argv[2], encrypt, &iv, &iv_len );

            if (ctx == 0) {
                fprintf( stderr, "Error in context setup, aborting.\n" );
                return 1;
            }
        }
    }

    for (;;) {
        out_len = sizeof( out );
        in_len = read( 0, in, sizeof(in) );

        if (in_len == -1) {
            fprintf( stderr, "Error while reading from stdin\n" );
            return 2;
        }
        else if (in_len != 0) {
            EVP_CipherUpdate( ctx, out, &out_len, in, in_len );

            write( 1, out, out_len );
        }
        else {
            EVP_CipherFinal( ctx, out, &out_len );

            write( 1, out, out_len );
            break;
        }
    }

    return 0;
}
