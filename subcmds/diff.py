#
# Copyright (C) 2008 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from command import PagedCommand

class Diff(PagedCommand):
  common = True
  helpSummary = "Show changes between commit and working tree"
  helpUsage = """
%prog [<project>...]
"""
  helpDescription = """
%prog show changes between commit and working tree.

The -u option causes '%prog' to generate diff output with file paths
relative to the repository root, so the output can be applied
to the Unix 'patch' command.

The -G <git_args> option can be used to pass additional arguments to git diff.

Example
-------

  - diff with only staged changes
    repo diff -u -r "^(kernel|lk|mdm.{4})$" -G "--cached"
"""

  def _Options(self, p):
    def cmd(option, opt_str, value, parser):
      setattr(parser.values, option.dest, list(parser.rargs))
      while parser.rargs:
        del parser.rargs[0]
    p.add_option('-u', '--absolute',
                 dest='absolute', action='store_true',
                 help='Paths are relative to the repository root')
    p.add_option('-r', '--regex',
                 dest='regex', action='store_true',
                 help="Execute the command only on projects matching regex or wildcard expression")
    p.add_option('-i', '--inverse-regex',
                 dest='inverse_regex', action='store_true',
                 help="Execute the command only on projects not matching regex or wildcard expression")
    p.add_option('-g', '--groups',
                 dest='groups',
                 help="Execute the command only on projects matching the specified groups")
    p.add_option('-G', '--gitargs',
                 type='string',  action='store', dest='git_args',
                 help='Additional git arguments to pass to git diff')

  def Execute(self, opt, args):

    if opt.regex:
      projects = self.FindProjects(args)
    elif opt.inverse_regex:
      projects = self.FindProjects(args, inverse=True)
    else:
      projects = self.GetProjects(args, groups=opt.groups)
    for project in projects:
      project.PrintWorkTreeDiff(opt.absolute, opt.git_args)
