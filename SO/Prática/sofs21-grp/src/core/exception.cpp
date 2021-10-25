/*
 * \file
 * \brief the sofs21 exception class
 * \author Artur Pereira - 2016-2020
 */

#include <exception>

#include <stdio.h>
#include <string.h>

#include "exception.h"

namespace sofs21
{
    /*
     * \brief sofs21 exception data type
     */
    SOException::SOException(int _en, const char *_func) 
            : en(_en), func(_func)
    {
        sprintf(msg, "\e[01;31m%s: error %d (%s)\e[0m", func, en, strerror(en));
    }

    const char *SOException::what() const throw()
    {
        return msg;
    }
};
