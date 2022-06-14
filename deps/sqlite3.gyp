# ===
# This configuration defines options specific to compiling SQLite3 itself.
# Compile-time options are loaded by the auto-generated file "defines.gypi".
# The --sqlite3 option can be provided to use a custom amalgamation instead.
# ===

{
  'includes': ['common.gypi'],
  'targets': [
    {
      'target_name': 'locate_sqlite3',
      'type': 'none',
      'hard_dependency': 1,
      'conditions': [
        ['sqlite3 == ""', {
          'actions': [{
            'action_name': 'copy_builtin_sqlite3',
            'inputs': [
              'sqlite3/sqlite3.c',
              'sqlite3/sqlite3.h',
              'sqlite3/sqlite3ext.h',
              'sqlite3/fts3_tokenizer.h',
              'sqlite3/mm_cipher.c',
              'sqlite3/mm_fts.h',
              'sqlite3/mm_sqliteext.c',
              'sqlite3/mm_tokenizer.c',
              'sqlite3/mm_utils.c',
            ],
            'outputs': [
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/sqlite3.c',
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/sqlite3.h',
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/sqlite3ext.h',
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/fts3_tokenizer.h',
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/mm_cipher.c',
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/mm_fts.h',
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/mm_sqliteext.c',
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/mm_tokenizer.c',
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/mm_utils.c',
            ],
            'conditions': [
              ['OS == "win"', {
                'outputs': [
                  '<(SHARED_INTERMEDIATE_DIR)/sqlite3/>(openssl_root)/libssl.lib',
                  '<(SHARED_INTERMEDIATE_DIR)/sqlite3/>(openssl_root)/libcrypto.lib',
                  '<(SHARED_INTERMEDIATE_DIR)/sqlite3/>(icu_root)/lib/icuuc.lib',
                  '<(SHARED_INTERMEDIATE_DIR)/sqlite3/>(icu_root)/lib/icuin.lib',
                ],
              }],
            ],
            'action': ['node', 'extract.js', '<(SHARED_INTERMEDIATE_DIR)/sqlite3', ''],
          }],
        }],
      ],
    },
    {
      'target_name': 'copy_dll',
      'type': 'none',
      'dependencies': ['locate_sqlite3'],
      'conditions': [
        ['OS == "win"', {
          'copies': [{
            'files': [
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/>(openssl_root)/libssl.lib',
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/>(openssl_root)/libcrypto.lib',
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/>(icu_root)/lib/icuuc.lib',
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/>(icu_root)/lib/icuin.lib',
            ],
            'destination': '<(PRODUCT_DIR)',
          }],
        }],
      ],
    },
    {
      'target_name': 'sqlite3',
      'type': 'static_library',
      'dependencies': ['locate_sqlite3', 'copy_dll'],
      'sources': [
        '<(SHARED_INTERMEDIATE_DIR)/sqlite3/sqlite3.c',
        '<(SHARED_INTERMEDIATE_DIR)/sqlite3/mm_cipher.c',
        '<(SHARED_INTERMEDIATE_DIR)/sqlite3/mm_sqliteext.c',
        '<(SHARED_INTERMEDIATE_DIR)/sqlite3/mm_tokenizer.c',
        '<(SHARED_INTERMEDIATE_DIR)/sqlite3/mm_utils.c',
      ],
      'include_dirs': [
        '<(SHARED_INTERMEDIATE_DIR)/sqlite3/',
        '<(SHARED_INTERMEDIATE_DIR)/sqlite3/openssl-include',
        '<(SHARED_INTERMEDIATE_DIR)/sqlite3/icu_include',
      ],
      'direct_dependent_settings': {
        'include_dirs': [
          '<(SHARED_INTERMEDIATE_DIR)/sqlite3/',
          '<(SHARED_INTERMEDIATE_DIR)/sqlite3/openssl-include',
          '<(SHARED_INTERMEDIATE_DIR)/sqlite3/icu_include',
        ],
      },
      'cflags': ['-std=c99', '-w'],
      'xcode_settings': {
        'OTHER_CFLAGS': ['-std=c99'],
        'WARNING_CFLAGS': ['-w'],
      },
      'conditions': [
        ['sqlite3 == ""', {
          'includes': ['defines.gypi'],
        }, {
          'defines': [
            # This is currently required by better-sqlite3.
            'SQLITE_ENABLE_COLUMN_METADATA',
          ],
        }],
        ['OS == "win"', {
          'defines': [
            'WIN32'
          ],
          'link_settings': {
            'libraries': [
              '-llibcrypto.lib',
              '-llibssl.lib',
              '-lws2_32.lib',
              '-lcrypt32.lib',
              '-licuuc.lib',
              '-licuin.lib'
            ],
            'library_dirs': [
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/>(openssl_root)',
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/>(icu_root)/lib/'
            ]
          }
        },
        'OS == "mac"', {
          'link_settings': {
            'libraries': [
              # This statically links libcrypto, whereas -lcrypto would dynamically link it
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/OpenSSL-macOS/libcrypto.a'
            ]
          }
        },
        { # Linux
          'link_settings': {
            'libraries': [
              # This statically links libcrypto, whereas -lcrypto would dynamically link it
              '<(SHARED_INTERMEDIATE_DIR)/sqlite3/OpenSSL-Linux/libcrypto.a'
            ]
          }
        }],
      ],
      'configurations': {
        'Debug': {
          'msvs_settings': { 'VCCLCompilerTool': { 'RuntimeLibrary': 1 } }, # static debug
        },
        'Release': {
          'msvs_settings': { 'VCCLCompilerTool': { 'RuntimeLibrary': 0 } }, # static release
        },
      },
    },
  ],
}
