#!/usr/bin/env python
""" formatters.py - collection of formatting utilities

"""

import re
from bs4 import BeautifulSoup
from docx.shared import Inches, Pt

def reduceWidth(rawText, maxWidth, cleanUp=False):
    """ formats text by preserving indentation

    rawText  -> the text we want to re-format
    maxWidth -> the maximum number of characters per line we want to format
    cleanup  -> cleans up raw text when true

    return formatted text
    """

    if cleanUp:
        rawText = rawText.replace("\n ", "\n")
        soup = BeautifulSoup(rawText, features="lxml")
        rawText = soup.get_text().replace(u"\xa0", u" ").replace("<br/>\n", "\n")
        
    formattedText = ""

    for line in rawText.split("\n"):
        formattedLine = ""
        indent = ""

        """ Get indentation of existing section, capture indented string length
        Line can start with spaces or without spaces followed by any of the
        following cases:
            1. Any digit and dot(.) combinations
            2. underscore(_)
            3. [, -
        Taking non greedy match by restricting greedy match with ?, stops 
        regex until the initial short match followed by zero or more spaces
        Storing the above match and using the length to preserve indentation
        Regex followed by any character or " or [ using non greedy match 
        """

        matchingPattern = re.search(r'(^\s*[\d.\-\_\[]*?\s*)[a-zA-Z\"\[?].*',
                                    line, re.I)
        if matchingPattern:
            indent = " " * len(matchingPattern.group(1))

        # split long lines into words and reassemble     
        if len(line) > maxWidth:
            for word in line.split(" "):
                if len(word) > maxWidth:
                    newWord = ""
                    # handles cases where words don't have spaces between them
                    for chars in word.split(","):
                        if len(formattedLine) + len(chars) <= maxWidth:
                            # length OK, add word
                            formattedLine = formattedLine + str(chars) + ","
                        else:
                            newWord = newWord + str(chars) + ","

                    formattedLine = f'{formattedLine.rstrip(" ")}\n'
                    formattedText = formattedText + formattedLine
                    formattedLine = indent + newWord.rstrip(",") + " "
                    continue
                # check if adding the word makes line too long
                if len(formattedLine) + len(word) <= maxWidth:
                    # length OK, add word
                    formattedLine = formattedLine + str(word) + " "

                else:
                    # too long add cuurent line to formatted text
                    formattedLine = f'{formattedLine.rstrip(" ")}\n'
                    formattedText = formattedText + formattedLine
                    formattedLine = indent + word + " "
        else:
            formattedText = formattedText + line
        formattedText += formattedLine + "\n"
    return formattedText


def getMaxCharWidth(cellWidthEmus, fontSizeEmus, scaling=0.95):
    """gives maximum width of characters in a column after converting cell
    width to inches and font size to pt 
    """
    
    return (cellWidthEmus / Inches(1)) * (120 / (fontSizeEmus / Pt(1))) * scaling


if __name__ == '__main__':

    # HELIX-16516
    # rawText = """taskSwapHookAttach shall perform the following in sequence:\n1. Use local ix of type int.\n2. Perform the actions defined by macro [KERNEL_ENTER].\n3. Loop from local ix equal zero to ix less than [VX_MAX_TASK_SWAP_RTNS]    \n     3.1. If [taskSwapTable[ix]] is equal [swapHook] then do the following: \n           3.1.1. Increment [taskSwapReference[ix]] by one if [in] is [TRUE] \n           3.1.2. Increment [taskSwapReference[ix]] by one if [out] is [TRUE] \n           3.1.3. If return value of Invoking function [taskSwapMaskSet] with 4 parameters: [tid], ix , [in], and [out] is not [OK] then do the following\n                    a) Decrement [taskSwapReference[ix] by one if [in] is [TRUE] \n                    b) Decrement [taskSwapReference[ix] by one if [out] is [TRUE] \n                    c) Perform the actions defined by macro [KERNEL_EXIT]\n                    d) return [ERROR] \n     3.2. Otherwise, Perform the actions defined by macro [KERNEL_EXIT], and return [OK]."""
    # rawText = """taskOpen - open a task<br/>\n <br/>\nThis routine opens an existing task specified by [name] or creates an newly task if [name] does not match the name of any existing task.<br/>\nThis routine returns ID of the task specified by [name] if:<br/>\n\xa0 \xa0 - [name] matches the name of an existing task and<br/>\n\xa0 \xa0 - [OM_CREATE] and [OM_EXCL] are not set in [mode].<br/>\nThis routine creates a task and returns ID of the new task if [OM_CREATE] is set in [mode].\xa0the new task is set the following properties:<br/>\n\xa0 \xa0 - [name] as the name of new task<br/>\n\xa0 \xa0 - [priority] as the priority of\xa0new task<br/>\n\xa0 \xa0 - [options] as the options of new task<br/>\n\xa0 \xa0 \xa0 \xa0 - the newly created task does not have stack protection if [VX_NO_STACK_PROTECT] is set in [options]<br/>\n\xa0 \xa0 \xa0 \xa0 - the stack of the\xa0newly created task is not filled with 0xee if\xa0[VX_NO_STACK_FILL] is set in [options]<br/>\n\xa0 \xa0 \xa0 \xa0 - the newly created task supports floating-point coprocessor\xa0if:<br/>\n\xa0 \xa0 \xa0 \xa0 \xa0 \xa0 - current task is not a kernel task or<br/>\n\xa0 \xa0 \xa0 \xa0 \xa0 \xa0 - current task is a kernel task and [VX_NO_FP_TASK] is not set in [options].<br/>\n \xa0 \xa0 \xa0 \xa0 - the newly created task is not support floating-point coprocessor\xa0if [VX_NO_FP_TASK] is set in [options]<br/>\n \xa0 \xa0 - [pStackBase] as the base of new task&#39;s execution stack<br/>\n \xa0 \xa0 - [stackSize]\xa0as\xa0the\xa0size\xa0(bytes)\xa0of\xa0stack\xa0needed<br/>\n \xa0 \xa0 - [entryPt]\xa0as\xa0the\xa0entry\xa0point\xa0of\xa0new\xa0task<br/>\n \xa0 \xa0 - [arg1],[arg2],[arg3],[arg4],[arg5],[arg6],[arg7],[arg8],[arg9],[arg10]\xa0as\xa0the\xa0arguments\xa0to\xa0pass to the new task.<br/>\n \xa0 \xa0 - if\xa0[mode]\xa0has\xa0[OM_CREATE]\xa0set\xa0and\xa0[name]\xa0does\xa0not\xa0match\xa0an\xa0existing\xa0public task name.<br/>\n <br/>\nThis routine returns [TASK_ID_NULL] and [errno] is set to:<br/>\n \xa0 \xa0 - [S_objLib_OBJ_INVALID_ARGUMENT], if [name] is [NULL] or [name] is an empty string.\xa0<br/>\n \xa0 \xa0 - [S_intLib_NOT_ISR_CALLABLE], if called from interrupt level.\xa0<br/>\n \xa0 \xa0 - [S_objLib_OBJ_INVALID_ARGUMENT], if [mode] includes undefined mode (only [OM_CREATE], [OM_EXCL] and [OM_DELETE_ON_LAST_CLOSE] are defined).<br/>\n \xa0 \xa0 - [S_objLib_OBJ_NOT_FOUND], if task\xa0with\xa0name\xa0[name]\xa0does\xa0not\xa0exist\xa0and [OM_CREATE] is not set in [mode].<br/>\n \xa0 \xa0 - [S_taskLib_NOT_ENOUGH_EXC_STACK], if:<br/>\n \xa0 \xa0 \xa0 \xa0 - [OM_CREATE] is set in [mode] and<br/>\n \xa0 \xa0 \xa0 \xa0 - the task with name [name] does not exist and\xa0<br/>\n \xa0 \xa0 \xa0 \xa0 - the default kernel exception stack size [TASK_KERNEL_EXC_STACK_SIZE] is not enough to create a new task.<br/>\n \xa0 \xa0 - [S_objLib_OBJ_NAME_CLASH], if:<br/>\n\xa0 \xa0 \xa0 \xa0 - [name] is start with &#39;/&#39; and <br/>\n\xa0 \xa0 \xa0 \xa0 - the task with name [name] does not exist and <br/>\n\xa0 \xa0 \xa0 \xa0 - [OM_CREATE] and [OM_EXCL] are set in [mode].<br/>\n \xa0 \xa0 - [S_taskLib_ILLEGAL_PRIORITY], if:<br/>\n \xa0 \xa0 \xa0 \xa0 - [OM_CREATE] is set in [mode] and<br/>\n \xa0 \xa0 \xa0 \xa0 - the task with name [name] does not exist and<br/>\n \xa0 \xa0 \xa0 \xa0 -\xa0[priority] is less than [VX_TASK_PRIORITY_MIN] or greater than [VX_TASK_PRIORITY_MAX].<br/>\n <br/>\nThis routine is the most general purpose task creation routine. It can also be used to obtain a task ID to an already existing task, typically a public task with an RTP. It searches the task name space for a matching task. If a matching task is found, it returns the task ID of the matched task. If a matching task is not found but the [OM_CREATE] flag is specified in the parameter, then it creates a task. This routine is not ISR callable. <br/>\n <br/>\nThere are two name spaces available in which [taskOpen] can perform the search. The name space searched is dependent upon the first character in the parameter. When this character is a forward slash &#39;/&#39;, the &#39;public&#39; name space is searched; otherwise the &#39;private&#39; name space is searched. Similarly, if a task is created, the &#39;s first character specifies the name space that contains the task. <br/>\n <br/>\nUnlike other objects in VxWorks, private task names are not unique. Thus a search on a private name space finds the first matching task. However, this task may not be the only task with the specified name. Public task names on the other hand, are unique."""
    rawText = """startupCpuThreads shall:<br/>\n\xa0- set pStartThr equal to [usrAppStartupThr]<br/>\n\xa0- loop while pStartThr-&gt;entry is not equal to [NULL]<br/>\n\xa0 \xa0- if pStartThr-&gt;cpuId is equal to [cpuNum] or pStartThr-&gt;cpuId is equal to [WRHV_START_CORE_ALL]<br/>\n\xa0 \xa0 \xa0- invoke [threadCreate] with parameters:\xa0<br/>\n\xa0 \xa0 \xa0 \xa0- pStartThr-&gt;name<br/>\n\xa0 \xa0 \xa0 \xa0- pStartThr-&gt;entry<br/>\n\xa0 \xa0\xa0\xa0 \xa0- pStartThr-&gt;priority<br/>\n\xa0 \xa0 \xa0\xa0\xa0- [THREAD_OPTION_NONE]<br/>\n\xa0 \xa0 \xa0\xa0\xa0- [NULL]<br/>\n\xa0 \xa0 \xa0\xa0\xa0- pStartThr-&gt;stackSize<br/>\n\xa0 \xa0 \xa0- set pid equal to the value returned from the invocation of [threadCreate]<br/>\n\xa0 \xa0 \xa0- if pid is not equal to [INVALID_CTX_ID]<br/>\n\xa0 \xa0 \xa0 \xa0- invoke [contextCpuSet] with parameters:<br/>\n\xa0 \xa0 \xa0 \xa0 \xa0- pid<br/>\n\xa0 \xa0 \xa0 \xa0 \xa0- [cpuNum]<br/>\n\xa0 \xa0 \xa0 \xa0- if the return value of the invocation of [contextCpuSet] with parameters (pid, [cpuNum]) is equal to [ERROR]<br/>\n\xa0 \xa0 \xa0 \xa0 \xa0- invoke [wrhvEvent] with parameters:<br/>\n\xa0 \xa0 \xa0 \xa0 \xa0 \xa0- [ctx-&gt;id]<br/>\n\xa0 \xa0 \xa0 \xa0 \xa0 \xa0- [WRHV_EVENT_HV_NONFATAL_KERNEL]<br/>\n\xa0 \xa0 \xa0 \xa0 \xa0 \xa0- &quot;startupCpuThreads.contextCpuSet().usrApp: Failed!!!&quot;<br/>\n\xa0 \xa0 \xa0 \xa0 \xa0- set result equal to [ERROR]<br/>\n\xa0 \xa0 \xa0 \xa0- invoke [schedulerAdd] with parameter pid<br/>\n\xa0 \xa0 \xa0 \xa0- if the return value of the invocation of [schedulerAdd] is equal to [ERROR]<br/>\n\xa0 \xa0 \xa0 \xa0 \xa0- invoke [wrhvEvent] with parameters:<br/>\n\xa0 \xa0 \xa0 \xa0 \xa0 \xa0- [ctx-&gt;id]<br/>\n\xa0 \xa0 \xa0 \xa0 \xa0 \xa0- [WRHV_EVENT_HV_NONFATAL_KERNEL],<br/>\n\xa0 \xa0 \xa0 \xa0 \xa0 \xa0- &quot;startupCpuThreads.schedulerAdd().usrApp: Failed!!!&quot;<br/>\n\xa0 \xa0 \xa0 \xa0 \xa0<span style="font-size: 10pt;line-height: 1.5;">- perform the actions defined by macro [st_printf] using values (&quot;%s: unable to start thread \\&quot;%s\\&quot; on cpu %d\\n&quot;, [ctx-&gt;name], pStartThr-&gt;name, [cpuNum])</span><br/>\n\xa0 \xa0 \xa0 \xa0 \xa0- set result equal to [ERROR]<br/>\n\xa0 \xa0 \xa0- else<br/>\n\xa0 \xa0 \xa0 \xa0- invoke [wrhvEvent] with parameters:<br/>\n\xa0 \xa0 \xa0 \xa0 \xa0- [ctx-&gt;id]<br/>\n\xa0 \xa0 \xa0 \xa0 \xa0- [WRHV_EVENT_HV_NONFATAL_KERNEL],<br/>\n\xa0 \xa0 \xa0 \xa0 \xa0- &quot;startupCpuThreads().usrApp: Thread Create Failed!!!&quot;<br/>\n\xa0 \xa0 \xa0 \xa0- set result equal to [ERROR]<br/>\n\xa0 \xa0- set pStartThr to next entry in [usrAppStartupThr]<br/>\n\xa0- continue\xa0loop\xa0([startupCpuThreads_LLR_5])"""

    for maxWidth in [60]:
        formattedText = reduceWidth(rawText, maxWidth, cleanUp=True)
        print(formattedText)