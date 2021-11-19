// Author: André Zúquete <andre.zuquete@ua.pt>

#include <stdio.h>
#include <stdint.h>
#include <memory.h>

#include <openssl/evp.h>
#include <openssl/rand.h>

#include "key.h"

// Set encryption / decryption context for AES block ciphers and ChaCha20 stream cipher
// For decryptions with IV it must be called twice

EVP_CIPHER_CTX *
set_ctx( char * password, char * algorithm, int encrypt, uint8_t ** iv, int * iv_len )
{
    int key_len;
    uint8_t * key;
    EVP_CIPHER_CTX * ctx;
    const EVP_CIPHER * alg;

    // Decryption?

    if (encrypt == 0) {
         // Null IV buffer => first call

         if (*iv == 0) {
            // Stream cipher? Must provide an IV buffer and its length

            if (strcmp( algorithm, "ChaCha20" ) == 0) {
                fprintf( stderr, "Set IV dimensions for ChaCha20\n" );
                *iv_len = 12;
                *iv = malloc( *iv_len );
            
                // That's all for now, the next call (with the IV) will set the context

                return 0;
            }
        }
    }
    else {
        *iv = 0;
    }

    ctx = EVP_CIPHER_CTX_new ();

    if (strcmp( algorithm, "AES-128" ) == 0) {
        key_len = 16;
        alg = EVP_aes_128_ecb();
        EVP_CIPHER_CTX_set_padding( ctx, 1 );
    }
    else if (strcmp( algorithm, "AES-192" ) == 0) {
        key_len = 24;
        alg = EVP_aes_192_ecb();
        EVP_CIPHER_CTX_set_padding( ctx, 1 );
    }
    else if (strcmp( algorithm, "AES-256" ) == 0) {
        key_len = 32;
        alg = EVP_aes_256_ecb();
        EVP_CIPHER_CTX_set_padding( ctx, 1 );
    }
    else if (strcmp( algorithm, "ChaCha20" ) == 0) {
        key_len = 20;
        *iv_len = 12;
        alg = EVP_chacha20();

        // For encryption use a random IV

        if (encrypt) {
            *iv = malloc( *iv_len );
            RAND_bytes( *iv, *iv_len );
        }
    }
    else {
        fprintf( stderr, "Algorithm must be one of these: AES-128, AES-192, AES-256, ChaCha20\n" );
        return 0;
    }

    key = malloc( key_len );

    PKCS5_PBKDF2_HMAC( password, strlen( password ), 0, 0, 100000, EVP_sha256(), key_len, key );

    EVP_CipherInit( ctx, alg, key, *iv, encrypt );

    return ctx;
}
