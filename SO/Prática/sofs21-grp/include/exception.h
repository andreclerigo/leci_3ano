/**
 * \file 
 * \brief The \b sofs21 exception devtools
 * \author Artur Pereira - 2016-2020
 */
#ifndef __SOFS21_EXCEPTION__
#define __SOFS21_EXCEPTION__

#include <exception>

namespace sofs21
{

    /** @{ */

    /**
     * \brief The \b sofs21 exception class
     * \ingroup exception
     */
    class SOException:public std::exception
    {
      public:
        int en;                 ///< (system) error number
        const char *func;       ///< name of function that has thrown the exception
        char msg[100];          ///< buffer to store the exception message

        /**
         * \brief the constructor
         * \param _en (system) error number 
         * \param _func name of function throwing the exception
         */
         SOException(int _en, const char *_func);

        /**
         * \brief default exception message
         * \return pointer to exception message
         */
        const char *what() const throw();
    };

    /** @} */

};

#endif /* __SOFS21_EXCEPTION__ */
